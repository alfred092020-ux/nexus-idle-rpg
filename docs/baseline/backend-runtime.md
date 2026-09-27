# Mirra Backend Runtime Baseline

Pinned SHA: `03ce82842a5d2d36f3a58396e7f22e0a43dfcb86`
Overall: `BLOCKED_DEP`

| Status | Check | Reason | Artifact |
| --- | --- | --- | --- |
| PASS | `git rev-parse HEAD` | backend SHA matches 03ce82842a5d2d36f3a58396e7f22e0a43dfcb86 | - |
| BLOCKED_DEP | `nix` | required executable missing: nix | - |
| BLOCKED_DEP | `devenv` | required executable missing: devenv | - |
| BLOCKED_DEP | `elixir` | required executable missing: elixir | - |
| BLOCKED_DEP | `mix` | required executable missing: mix | - |
| PASS | `protoc` | found protoc at /usr/bin/protoc | - |
| BLOCKED_DEP | `psql` | required executable missing: psql | - |

A missing host prerequisite is BLOCKED_DEP. A wrong checkout or a command/test failure is FAIL. No privileged dependency installation is performed by this probe.
