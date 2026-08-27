# Trigger index

Archived in Cleanup Patch C3:

- root `.powder-*` trigger files for API probe/smoke, cleanup, observer, handover, H-calibration, lifecycle, discovery, SSH/plumbing checks;
- `.wp2-b-create-trigger` from the old one-off create path;
- `.wp2-h-early-window-trigger` from the live allocation path;
- `powder/g3-trigger.json`;
- `powder/wp2-powder-status.trigger`.

Current local/static triggers remain in place only where their associated active workflow has no POWDER resource interaction.
