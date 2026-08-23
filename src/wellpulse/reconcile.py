def reconcile_ids(generated_ids, received_ids):
    generated = list(generated_ids)
    received = list(received_ids)
    gs, rs = set(generated), set(received)
    return {
        "generated": len(generated),
        "received_total": len(received),
        "received_unique": len(rs),
        "missing": sorted(gs-rs),
        "unexpected": sorted(rs-gs),
        "duplicates": len(received)-len(rs),
        "completeness_pct": 100.0 if not generated else 100.0*len(gs & rs)/len(gs),
    }
