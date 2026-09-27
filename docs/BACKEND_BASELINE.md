# Mirra Backend Baseline

Nexus Idle keeps the Mirra backend external during foundation certification. The client repository records and verifies an exact reviewed backend SHA instead of vendoring backend source.

## Pinned upstream

- Repository: `https://github.com/lambdaclass/mirra_backend.git`
- Reviewed branch: `main`
- Reviewed commit: `03ce82842a5d2d36f3a58396e7f22e0a43dfcb86`
- Local dependency path: `.nexus/deps/mirra_backend`
- Checkout mode: detached HEAD at the reviewed commit

From the Nexus Idle repository root:

```bash
python3 -m tools.foundation.backend_pin \
  --pin config/upstreams/mirra-backend.json \
  --dest .nexus/deps/mirra_backend \
  --verify
```

The command clones or refreshes the external checkout, checks out the exact reviewed SHA detached, and fails if origin or HEAD does not match the pin.

## Prerequisites at the reviewed SHA

The pinned Mirra README requires Nix first, then devenv. The repository's `.tool-versions` records Elixir `1.16.3-otp-26` and Erlang `26.2.5.5`.

The pinned `devenv.nix` supplies GNU Make, protobuf, Rust/Cargo, Clang, Node.js 21, Elixir 1.16 on Erlang/OTP 26, JavaScript support, and PostgreSQL 16. Linux also receives `inotify-tools`.

The development PostgreSQL service listens on `127.0.0.1:5432`. The devenv baseline creates the `postgres` user and the `game_backend_prod` database for local development.

Mirra's setup guide also installs Hex through Mix:

```bash
devenv shell
mix archive.install github hexpm/hex branch latest
```

Protobuf is required for WebSocket message serialization. The upstream guide installs the protobuf compiler plus the Elixir protobuf escript. Its JS client setup uses `google-protobuf` and `protoc-gen-js` under `assets/`.

## Startup baseline

The upstream full-stack development path is:

```bash
devenv up
```

For an interactive Elixir workflow, the upstream documents starting PostgreSQL through devenv, then starting the applications from a devenv shell:

```bash
devenv shell postgres
# separate terminal
devenv shell
make start
```

The root Mix project is an umbrella application. Its setup alias runs dependency fetch plus Ecto database creation, migration, and seed steps. Test setup resets and migrates the test databases before running tests.

This document records repository evidence only. Later foundation tasks must probe whether the required Nix/devenv/PostgreSQL environment is available on Nexus infrastructure and report missing environment dependencies as `BLOCKED_DEP`, not as a product failure.
