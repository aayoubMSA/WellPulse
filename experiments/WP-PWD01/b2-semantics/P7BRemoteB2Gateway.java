import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.time.Instant;
import java.util.concurrent.atomic.AtomicBoolean;

import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttAsyncClient;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MqttDefaultFilePersistence;

/**
 * WP2-P7B non-scored remote-capable B2 gateway.
 *
 * The separate generator writes newline-delimited canonical payloads to a FIFO.
 * This gateway owns the Paho durable-client state and is the only process in the
 * intentional S3 restart domain.
 */
public final class P7BRemoteB2Gateway {
    private static final String PAHO_VERSION = "1.2.5";
    private static final int BUFFER_SIZE = 4096;
    private static final AtomicBoolean STOP = new AtomicBoolean(false);

    private static SSLSocketFactory socketFactory(Path caFile) throws Exception {
        CertificateFactory factory = CertificateFactory.getInstance("X.509");
        Certificate ca;
        try (FileInputStream in = new FileInputStream(caFile.toFile())) {
            ca = factory.generateCertificate(in);
        }
        KeyStore store = KeyStore.getInstance(KeyStore.getDefaultType());
        store.load(null, null);
        store.setCertificateEntry("wellpulse-p7b-ca", ca);
        TrustManagerFactory managers =
            TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        managers.init(store);
        SSLContext context = SSLContext.getInstance("TLS");
        context.init(null, managers.getTrustManagers(), null);
        return context.getSocketFactory();
    }

    private static MqttConnectOptions connectOptions(Path caFile) throws Exception {
        MqttConnectOptions options = new MqttConnectOptions();
        options.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1_1);
        options.setCleanSession(false);
        options.setAutomaticReconnect(false);
        options.setKeepAliveInterval(60);
        options.setConnectionTimeout(5);
        options.setSocketFactory(socketFactory(caFile));
        return options;
    }

    private static MqttAsyncClient build(
        String broker, String clientId, Path persistenceDir
    ) throws Exception {
        Files.createDirectories(persistenceDir);
        MqttDefaultFilePersistence persistence =
            new MqttDefaultFilePersistence(persistenceDir.toString());
        MqttAsyncClient client = new MqttAsyncClient(broker, clientId, persistence);
        DisconnectedBufferOptions buffer = new DisconnectedBufferOptions();
        buffer.setBufferEnabled(true);
        buffer.setBufferSize(BUFFER_SIZE);
        buffer.setPersistBuffer(true);
        buffer.setDeleteOldestMessages(false);
        client.setBufferOpts(buffer);
        return client;
    }

    private static synchronized void event(
        Path log, String name, String fields
    ) {
        String safe = fields.replace("\\", "\\\\").replace("\"", "\\\"");
        String row = String.format(
            "{\"utc\":\"%s\",\"monotonic_ns\":%d,\"event\":\"%s\",\"detail\":\"%s\"}%n",
            Instant.now().toString(), System.nanoTime(), name, safe
        );
        try (BufferedWriter writer = Files.newBufferedWriter(
            log, StandardCharsets.UTF_8,
            java.nio.file.StandardOpenOption.CREATE,
            java.nio.file.StandardOpenOption.APPEND
        )) {
            writer.write(row);
        } catch (Exception exc) {
            throw new RuntimeException("cannot persist B2 event", exc);
        }
    }

    private static Thread reconnectWorker(
        MqttAsyncClient client, MqttConnectOptions options, Path eventLog
    ) {
        Thread worker = new Thread(() -> {
            while (!STOP.get()) {
                try {
                    if (!client.isConnected() && !client.isConnecting()) {
                        event(eventLog, "b2_connect_attempt", "paho=" + PAHO_VERSION);
                        client.connect(options).waitForCompletion(10000);
                    }
                } catch (Exception exc) {
                    event(eventLog, "b2_connect_retry", exc.getClass().getSimpleName());
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException exc) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        }, "p7b-b2-connect");
        worker.setDaemon(true);
        worker.start();
        return worker;
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 7) {
            throw new IllegalArgumentException(
                "usage: BROKER CLIENT_ID TOPIC PERSIST_DIR CA_FILE FIFO EVENT_LOG"
            );
        }
        String broker = args[0];
        String clientId = args[1];
        String topic = args[2];
        Path persistDir = Paths.get(args[3]);
        Path caFile = Paths.get(args[4]);
        Path fifo = Paths.get(args[5]);
        Path eventLog = Paths.get(args[6]);

        MqttAsyncClient client = build(broker, clientId, persistDir);
        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                event(eventLog, "b2_connect", "server=" + serverURI);
            }

            @Override
            public void connectionLost(Throwable cause) {
                event(
                    eventLog,
                    "b2_connection_lost",
                    cause == null ? "unknown" : cause.getClass().getSimpleName()
                );
            }

            @Override
            public void messageArrived(String incomingTopic, MqttMessage message) {
                event(eventLog, "b2_unexpected_inbound", incomingTopic);
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
                try {
                    event(eventLog, "b2_delivery_complete", "mid=" + token.getMessageId());
                } catch (Exception exc) {
                    event(eventLog, "b2_delivery_complete", "mid=unavailable");
                }
            }
        });

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            STOP.set(true);
            event(eventLog, "b2_gateway_shutdown", "pid=" + ProcessHandle.current().pid());
            try {
                if (client.isConnected()) {
                    client.disconnect().waitForCompletion(5000);
                }
                client.close();
            } catch (Exception exc) {
                event(eventLog, "b2_shutdown_error", exc.getClass().getSimpleName());
            }
        }));

        event(
            eventLog,
            "b2_gateway_start",
            "pid=" + ProcessHandle.current().pid()
                + ";paho=" + PAHO_VERSION
                + ";client_id=" + clientId
                + ";topic=" + topic
        );
        MqttConnectOptions options = connectOptions(caFile);
        reconnectWorker(client, options, eventLog);

        while (!STOP.get()) {
            try (BufferedReader reader = Files.newBufferedReader(fifo, StandardCharsets.UTF_8)) {
                String payload;
                while (!STOP.get() && (payload = reader.readLine()) != null) {
                    MqttMessage message =
                        new MqttMessage(payload.getBytes(StandardCharsets.UTF_8));
                    message.setQos(1);
                    message.setRetained(false);
                    client.publish(topic, message);
                    event(
                        eventLog,
                        "b2_publish_accepted",
                        "buffered_count=" + client.getBufferedMessageCount()
                    );
                }
            } catch (java.nio.file.NoSuchFileException exc) {
                event(eventLog, "b2_fifo_missing", fifo.toString());
            }
            Thread.sleep(100);
        }
    }
}
