# Independent P7B Preflight Review Checklist

Before QA closure, verify from the committed source itself:

- remote defaults resolve on the POWDER node, not the GitHub runner;
- no unresolved shell-token path is passed as a remote absolute path;
- self-audit cannot flag its own comments/string tables as runtime authority;
- SSH agent state is contained in one process;
- no Portal/RF/scientific/teardown action exists;
- pinned interpreter performs all project Python syntax/import checks;
- preservation proof uses shell primitives only;
- no workflow or trigger activates the probe;
- repository unit tests distinguish historical live-surface tests from this new offline probe.
