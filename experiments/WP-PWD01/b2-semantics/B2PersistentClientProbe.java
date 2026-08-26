import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.MqttAsyncClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MqttDefaultFilePersistence;

public final class B2PersistentClientProbe {
    private static final int RECORDS = 5;

    private static MqttAsyncClient build(String broker, String clientId, String persistDir) throws Exception {
        MqttDefaultFilePersistence persistence = new MqttDefaultFilePersistence(persistDir);
        MqttAsyncClient client = new MqttAsyncClient(broker, clientId, persistence);
        DisconnectedBufferOptions buffer = new DisconnectedBufferOptions();
        buffer.setBufferEnabled(true);
        buffer.setBufferSize(4096);
        buffer.setPersistBuffer(true);
        buffer.setDeleteOldestMessages(false);
        client.setBufferOpts(buffer);
        return client;
    }

    private static MqttConnectOptions options() {
        MqttConnectOptions options = new MqttConnectOptions();
        options.setCleanSession(false);
        options.setAutomaticReconnect(false);
        options.setKeepAliveInterval(5);
        options.setConnectionTimeout(5);
        return options;
    }

    private static void write(Path path, String value) throws Exception {
        Files.write(path, value.getBytes(StandardCharsets.UTF_8));
    }

    private static void phaseOutage(String broker, String clientId, String topic, String persistDir,
                                    Path ready, Path go, Path buffered) throws Exception {
        MqttAsyncClient client = build(broker, clientId, persistDir);
        client.connect(options()).waitForCompletion(10000);
        if (!client.isConnected()) throw new IllegalStateException("initial connect failed");
        write(ready, "connected\n");

        long goDeadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(30);
        while (!Files.exists(go)) {
            if (System.nanoTime() > goDeadline) throw new IllegalStateException("go flag timeout");
            Thread.sleep(50);
        }

        long disconnectDeadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(15);
        while (client.isConnected()) {
            if (System.nanoTime() > disconnectDeadline) throw new IllegalStateException("client did not detect broker outage");
            Thread.sleep(50);
        }

        for (int i = 1; i <= RECORDS; i++) {
            String payload = String.format("B2-R%04d", i);
            MqttMessage msg = new MqttMessage(payload.getBytes(StandardCharsets.UTF_8));
            msg.setQos(1);
            msg.setRetained(false);
            client.publish(topic, msg);
        }
        int count = client.getBufferedMessageCount();
        if (count != RECORDS) throw new IllegalStateException("expected 5 buffered messages, found " + count);
        write(buffered, Integer.toString(count) + "\n");
        Runtime.getRuntime().halt(0);
    }

    private static void phaseRecover(String broker, String clientId, String persistDir, Path result) throws Exception {
        MqttAsyncClient client = build(broker, clientId, persistDir);
        client.connect(options()).waitForCompletion(10000);
        if (!client.isConnected()) throw new IllegalStateException("recovery connect failed");

        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(20);
        while (client.getBufferedMessageCount() != 0) {
            if (System.nanoTime() > deadline) {
                throw new IllegalStateException("persistent disconnected buffer did not drain; count=" + client.getBufferedMessageCount());
            }
            Thread.sleep(100);
        }
        write(result, "buffered_after_recovery=0\n");
        client.disconnect().waitForCompletion(5000);
        client.close();
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 8) {
            throw new IllegalArgumentException("usage: MODE BROKER CLIENT_ID TOPIC PERSIST_DIR FLAG1 FLAG2 FLAG3");
        }
        String mode = args[0];
        String broker = args[1];
        String clientId = args[2];
        String topic = args[3];
        String persistDir = args[4];
        Path f1 = Paths.get(args[5]);
        Path f2 = Paths.get(args[6]);
        Path f3 = Paths.get(args[7]);

        if ("outage".equals(mode)) {
            phaseOutage(broker, clientId, topic, persistDir, f1, f2, f3);
        } else if ("recover".equals(mode)) {
            phaseRecover(broker, clientId, persistDir, f1);
        } else {
            throw new IllegalArgumentException("unknown mode: " + mode);
        }
    }
}
