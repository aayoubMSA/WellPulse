# WP2-P17V — Independent Claim Validation Matrix

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **INDEPENDENT VALIDATION COMPLETE / CLAIM ENVELOPE CONFIRMED**

## 1. Purpose

Provide a second, independent validation of the P17 consortium-revised manuscript against the primary scientific authorities rather than treating the first consortium verdict as evidence.

Validation authorities:

- P11 full raw-data scientific analysis;
- P12 cross-evidence integration;
- P13 frozen claim–evidence matrix;
- P16 adversarial publication QA and mandatory editorial constraints;
- canonical W1 source files `src/wellpulse/records.py` and `src/wellpulse/store.py`;
- P9 POWDER validity/anomaly/trace authorities where required;
- the P17 revised manuscript;
- independent current literature/baseline checks for MQTT persistence and testbed framing.

The validation does not authorize submission, add experiments, or expand the claim envelope.

## 2. Independent validation criteria

Each claim is tested against six gates:

1. **Numerical consistency** — manuscript value matches accepted analysis.
2. **Evidence authority** — value/statement traces to an accepted evidence class.
3. **Comparator/failure-domain boundary** — wording does not imply a stronger comparison than executed.
4. **Statistical discipline** — scientific unit, replication and uncertainty are represented honestly.
5. **Negative/anomalous evidence** — adverse or caveated evidence is not hidden.
6. **Publication wording** — the statement is understandable without internal project-control terminology.

## 3. Claim-by-claim validation

| Claim | Independent verdict | Validation finding | Residual condition |
|---|---|---|---|
| **IC-01 — FIT W1 vs B0 record survival** | **VALIDATED / A** | P17 preserves the exact C1/C2 80% vs 100% run-level outcomes and repeatedly identifies B0 as non-durable. The 2,000 missing B0 records align exactly with the imposed outage-period record block. | Must never be shortened to generic MQTT superiority. |
| **IC-02 — healthy FIT C0** | **VALIDATED / A** | P17 correctly states 10,000/10,000 for both architectures in all three C0 runs and does not infer universal equivalence. | Keep workload/platform boundary. |
| **IC-03 — W1 backlog-drain cost** | **VALIDATED / A** | Means `67.731246 s` and `67.870252 s` match P11; P17 clearly separates ~1.3 s reconnect from ~68 s backlog reconciliation. | Do not merge with POWDER recovery clocks. |
| **IC-04 — POWDER transition region** | **VALIDATED / B** | E1R4/E2/E3 values match accepted reconstruction; P17 consistently uses experiment-specific programmed attenuation and rejects a universal 52 dB threshold. | Unresolved attenuator-ID→physical-path mapping remains outside claims. |
| **IC-05 — ICMP degradation can precede MQTT incompleteness** | **VALIDATED / B** | E1R4 51 dB and E3 51 dB support the bounded cross-layer observation. P17 does not attribute this to W1. | Avoid generic “MQTT is more resilient than ICMP” wording. |
| **IC-06 — mechanism-dependent recovery** | **VALIDATED / B** | P17 keeps E10-A censored, E10-B/E10-C-B endpoint-specific, and E10-D upper-bound only. It also uses E4 versus E10-A to reject uniform RF-only recovery. | Prefer “not observed uniformly across preserved RF-only cases” if future editing risks implying identical treatments. |
| **IC-07 — broker-only failure isolation** | **VALIDATED / B** | E8 is correctly elevated: bidirectional ping remains healthy while MQTT delivery fails; duplicate sends are handled by unique receiver identities. | Remain a path-isolation control, not an architecture comparison. |
| **IC-08 — two-property failure-domain-aware synthesis** | **VALIDATED / C** | P17 makes FIT and POWDER explicitly non-overlapping in inferential role and integrates them only conceptually. | Do not claim this conceptual separation is historically unique without a dedicated novelty proof. |
| **IC-09 — receiver-side evidence-first reconciliation** | **VALIDATED / C** | P17 materially strengthens the methodological case with seq 96, seq 150, and E8 duplicate-send evidence while avoiding sender-only accounting. | Present as demonstrated methodology/practice, not universal theorem. |

## 4. Independent numerical spot-check

The following P17 values were rechecked against P11/P13 and passed:

- FIT C0: B0/W1 = 100%/100% in 3/3;
- FIT C1: B0/W1 = 80%/100% in 3/3;
- FIT C2: B0/W1 = 80%/100% in 3/3;
- outage-period generated records = 2,000;
- W1 backlog-drain means = `67.731246 s` and `67.870252 s`;
- E1R4 51 dB = ICMP loss 30%, MQTT 20/20;
- E1R4 52 dB = ICMP loss 60%, MQTT 13/20;
- E3 52 dB MQTT = 60%, 25%, 55%;
- E10-B = first publish `6.063318 s`, first ping `6.609430 s`, publish→CORE `0.060172 s`;
- E10-C-B = first ping `29.247733 s`, first publish `29.248129 s`;
- E10-D = `<=10.908749 s` upper bound only;
- E8 = 40/60 unique delivery with duplicate sender-line artifact preserved.

`P17V_NUMERICAL_CONTRADICTIONS=0`

## 5. Canonical implementation validation

P17's W1 implementation description is consistent with source:

- `record_id = run_id:boot_id:sequence` with zero-padded sequence;
- deterministic canonical JSON serialization;
- SHA-256 checksum per record;
- SQLite queue;
- `PRAGMA journal_mode=WAL`;
- `PRAGMA synchronous=FULL`;
- explicit `PENDING` / `SENT` state;
- exact duplicate re-enqueue is idempotent;
- conflicting reuse of an existing record ID raises `ValueError`.

The manuscript appropriately treats these as implementation facts explaining the evaluated semantics, not as independent empirical claims.

`P17V_IMPLEMENTATION_DESCRIPTION=PASS`

## 6. Independent baseline / prior-art validation

The second consortium independently confirmed the central baseline limitation:

- durable MQTT persistence is established prior art;
- Eclipse Paho Java provides pluggable/file persistence for reliable in-flight message delivery across network/client restarts;
- current Paho documentation explicitly warns that memory-only state can be lost on client/runtime/device shutdown;
- therefore B0 cannot be treated as representing the strongest standard durable MQTT configuration.

P17 handles this correctly by framing the FIT result as a durability effect relative to a non-durable baseline, not a generic protocol superiority claim.

The independent literature check also reconfirmed:

- store-and-forward over intermittent 5G/NTN is established prior art;
- FIT IoT-LAB literature emphasizes repeatable real-testbed experimentation;
- POWDER's published platform design explicitly targets controllable, end-to-end wireless experimentation and repeatability;
- Gaspar et al. 2026 and DOI `10.1109/MIOT.2026.3681190` are independently confirmed bibliographically, but detailed full-text comparison remains an open pre-submission gate.

`P17V_NOVELTY_BOUNDARY=VALIDATED_WITH_SUBMISSION_DATE_LITERATURE_GATE`

## 7. Independent risk rating

| Risk | Rating after P17V | Decision |
|---|---|---|
| Numerical/evidence contradiction | **LOW** | PASS |
| Statistical pseudoreplication | **LOW** | PASS |
| Overclaiming B0 result | **LOW–MODERATE** | Controlled by explicit comparator boundary |
| Durable-MQTT comparator absence | **MODERATE** | Transparent limitation; does not block bounded paper |
| FIT/POWDER stitched-study perception | **LOW–MODERATE** | Scientifically coherent; main-display redesign still recommended |
| POWDER manual/reference characterization | **MODERATE** | Defensible as descriptive characterization only |
| Recovery-clock ambiguity | **LOW** | Endpoint semantics are explicit |
| Receiver-vs-sender accounting | **LOW** | Strong methodological defense |
| Novelty over store-and-forward | **LOW–MODERATE** | Controlled; full literature gate still needed |
| Main-display cohesion | **MODERATE / OPEN** | P18 required |
| Supplement/artifact audit burden | **MODERATE / OPEN** | P19 required |
| Authorship/credits/funding/licensing | **OPEN** | Must be verified before submission |

## 8. Final independent verdict

**VALIDATED WITH PRE-SUBMISSION CONDITIONS.**

The P17 revised manuscript is scientifically coherent, numerically consistent with the accepted evidence, inside the P13 claim envelope, and materially stronger than P15. The second consortium did not identify a scientific reason to reopen experimentation or add a new empirical claim.

The paper is **not yet submission-ready** because the remaining gates are publication-preparation gates:

1. P18 main-display redesign and claim/display QA;
2. P19 reviewer supplement + sanitized artifact;
3. final submission-date literature check, including Gaspar full text if accessible;
4. final authorship/CRediT/funding/affiliation/testbed acknowledgments/copyright/licensing verification;
5. journal-specific formatting and final proof QA;
6. explicit submission authorization.

`P17V_CLAIMS_VALIDATED=9_OF_9`

`P17V_NUMERICAL_CONTRADICTIONS=0`

`P17V_UNSUPPORTED_NEW_CLAIMS=0`

`P17V_NEW_EXPERIMENT_REQUIRED=NO`

`P17V_VERDICT=VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`
