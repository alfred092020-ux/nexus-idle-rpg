# Nexus Idle RPG Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a legally traceable, reproducible, verified Game #2 foundation from Lambda-Forge's AFK Gacha Game without touching `main`, while keeping the Mirra backend external and proving existing systems before transformation.

**Architecture:** Build `feat/idle-rpg-foundation` from the reviewed Lambda commit so upstream ancestry remains intact, then merge the approved Nexus docs history. Add Python-stdlib foundation tools for provenance, dependency/license inventory, backend pinning, static audit, CI, and runtime probes; runtime results are PASS, FAIL, or BLOCKED_DEP rather than guesses.

**Tech Stack:** Git, Unity `2021.3.26f1`, C#, Python 3.12 stdlib, GitHub Actions, Mirra Backend (Elixir/Mix/Devenv/PostgreSQL), protobuf.

**Spec:** `docs/superpowers/specs/2026-09-26-nexus-idle-rpg-foundation-design.md`

## Global Constraints

- Never develop directly on `main`; canonical Game #2 integration branch is `feat/idle-rpg-foundation`.
- Preserve Lambda upstream history; do not squash or flatten imported client history.
- Reviewed Lambda baseline: `116227e448b8ba375fb4aef80db6dafa33232909`; re-check remote but never silently follow a newer commit.
- Reviewed Mirra baseline: `03ce82842a5d2d36f3a58396e7f22e0a43dfcb86`; backend remains external during foundation work.
- Preserve Apache-2.0 code notices and separately track graphics/music/Asset Store obligations.
- Never fetch/copy paid or proprietary Unity assets without a Nexus-owned license.
- Baseline claims require repository/runtime evidence; upstream milestones are context, not proof.
- Game #2 gets isolated Brain mission/task/lease/verification identity; Logres project facts must not leak into it.
- Worker edits require isolated branches/worktrees plus a live Brain lease.
- Verification order: changed tests → focused checks → build/static checks → integration/runtime → exact-SHA evidence → Android proof when applicable.

## Review Focus

1. **Upstream moved after review:** keep the reviewed SHA pinned and fail until an intentional review updates it.
2. **Shallow/incomplete history:** provenance verification fails clearly when the Lambda pin is absent/unreachable.
3. **Unknown/missing third-party license:** dependency audit reports `NEEDS_REVIEW` or `BLOCKED_DEP`, never runnable.
4. **Backend checkout at wrong SHA:** backend verification fails before client/backend results are trusted.
5. **Unity/Nix/PostgreSQL unavailable:** probes emit `BLOCKED_DEP`, not a false product failure/pass.

---

### Task 1: Establish the preserved-history integration root

**Files:**
- Existing: approved spec and this plan under `docs/superpowers/`
- Git refs created: `vendor/lambda-main`, `worker/nexus-idle-foundation-import-001`, `feat/idle-rpg-foundation`

**Interfaces:**
- Consumes: docs branch `docs/nexus-idle-foundation-spec-001` and Lambda remote `https://github.com/Lambda-Forge/afk_gacha_game.git`.
- Produces: integration HEAD containing Nexus docs with Lambda SHA `116227e...` as an ancestor.

- [ ] **Step 1: Re-check live Brain, active leases, Nexus Idle tasks, and current repo refs; expected no duplicate active Nexus Idle bootstrap work.**
- [ ] **Step 2: Acquire Brain lease `NEXUS-IDLE-FOUNDATION-IMPORT-001` on `worker/nexus-idle-foundation-import-001` before any edit.**
- [ ] **Step 3: Run `git ls-remote https://github.com/Lambda-Forge/afk_gacha_game.git refs/heads/main` and record the observed remote SHA without changing the reviewed pin.**
- [ ] **Step 4: Fetch the complete Lambda history into the isolated bootstrap workspace.**
- [ ] **Step 5: Run `git cat-file -e 116227e448b8ba375fb4aef80db6dafa33232909^{commit}`; expected exit 0.**
- [ ] **Step 6: Push the reviewed Lambda line to `origin/vendor/lambda-main`; expected ref points exactly to `116227e...`.**
- [ ] **Step 7: Create `worker/nexus-idle-foundation-import-001` at the reviewed Lambda SHA.**
- [ ] **Step 8: Merge `docs/nexus-idle-foundation-spec-001` using `--allow-unrelated-histories --no-ff`; expected candidate contains both source and approved docs.**
- [ ] **Step 9: Verify `git merge-base --is-ancestor 116227e448b8ba375fb4aef80db6dafa33232909 HEAD`, `client/ProjectSettings/ProjectVersion.txt`, and both approved docs files; expected PASS.**
- [ ] **Step 10: Push the verified candidate to `origin/feat/idle-rpg-foundation` without creating/updating `main`.**
- [ ] **Step 11: Record the exact integration SHA and import evidence in Brain.**

### Task 2: Add machine-verifiable client provenance

**Files:**
- Create: `config/upstreams/lambda-client.json`
- Create: `docs/UPSTREAM_PROVENANCE.md`
- Create: `tools/foundation/__init__.py`
- Create: `tools/foundation/provenance.py`
- Create: `tools/foundation/tests/test_provenance.py`

**Interfaces:**
- Produces: `UpstreamPin(repo_url: str, branch: str, commit: str, code_license: str)`.
- Produces: `load_pin(path: Path) -> UpstreamPin`, `verify_pin(repo_root: Path, pin_path: Path, ref: str = "HEAD") -> list[str]`, `ensure_remote(repo_root: Path, name: str, url: str) -> None`.

- [ ] **Step 1: Write tests for exact pin parsing, ancestor success, missing/unreachable commit, wrong upstream URL, and a moved remote branch that must not mutate the reviewed pin.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_provenance -v`; expected FAIL because implementation is absent.**
- [ ] **Step 3: Implement the interfaces and pin URL, branch `main`, SHA `116227e...`, Apache-2.0, and Unity `2021.3.26f1`.**
- [ ] **Step 4: Run `python3 -m unittest tools.foundation.tests.test_provenance -v`; expected PASS.**
- [ ] **Step 5: Run `python3 -m tools.foundation.provenance --repo . --pin config/upstreams/lambda-client.json --ref HEAD`; expected PASS.**
- [ ] **Step 6: Commit `chore: pin Lambda client provenance`.**

### Task 3: Pin Mirra backend without vendoring it

**Files:**
- Create: `config/upstreams/mirra-backend.json`
- Create: `tools/foundation/backend_pin.py`
- Create: `tools/foundation/tests/test_backend_pin.py`
- Modify: `.gitignore`
- Create: `docs/BACKEND_BASELINE.md`

**Interfaces:**
- Produces: `BackendPin(repo_url: str, branch: str, commit: str)`.
- Produces: `checkout_backend(pin: BackendPin, dest: Path) -> None` and `verify_checkout(pin: BackendPin, dest: Path) -> list[str]`.

- [ ] **Step 1: Write tests with a temporary local Git remote for fresh checkout, idempotent rerun, and wrong-HEAD rejection.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_backend_pin -v`; expected FAIL.**
- [ ] **Step 3: Implement exact pin `03ce82842a5d2d36f3a58396e7f22e0a43dfcb86`, cloning/fetching into `.nexus/deps/mirra_backend` and checking out detached SHA.**
- [ ] **Step 4: Add `.nexus/deps/` to `.gitignore`.**
- [ ] **Step 5: Document Mirra's Nix/devenv/Mix/protobuf/PostgreSQL prerequisites in `docs/BACKEND_BASELINE.md`.**
- [ ] **Step 6: Run `python3 -m unittest tools.foundation.tests.test_backend_pin -v`; expected PASS.**
- [ ] **Step 7: Run `python3 -m tools.foundation.backend_pin --pin config/upstreams/mirra-backend.json --dest .nexus/deps/mirra_backend --verify`; expected exact SHA PASS.**
- [ ] **Step 8: Commit `chore: pin external Mirra backend`.**

### Task 4: Build the Unity dependency and license inventory

**Files:**
- Create: `config/dependencies/unity-third-party.json`
- Create: `tools/foundation/dependencies.py`
- Create: `tools/foundation/tests/test_dependencies.py`
- Create: `docs/dependencies/unity-third-party.md`

**Interfaces:**
- Consumes: `client/Packages/manifest.json`, upstream README requirements, repository paths, and dependency manifest.
- Produces: `DependencyFinding(name: str, status: str, source: str, expected_path: str | None, license_state: str)` and `scan_dependencies(repo_root: Path, manifest_path: Path) -> list[DependencyFinding]`.

- [ ] **Step 1: Write tests proving unknown license => `NEEDS_REVIEW`, required missing asset => `BLOCKED_DEP`, and a UPM dependency is detected from `manifest.json`.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_dependencies -v`; expected FAIL.**
- [ ] **Step 3: Implement scanner/manifest for RPG & MMO UI 6, Map Maker, RPG inventory icons, Basic RPG Icons, Resource Vector Graphics, DOTween, Gold Mining Game, UX Flat Icons, TextMeshPro, and every UPM/Git package.**
- [ ] **Step 4: Generate `docs/dependencies/unity-third-party.md` with `PRESENT`, `MISSING`, `BLOCKED_DEP`, and `NEEDS_REVIEW`; never infer redistribution rights from file presence.**
- [ ] **Step 5: Run `python3 -m tools.foundation.dependencies --repo . --manifest config/dependencies/unity-third-party.json --mode inventory`; expected success only when every dependency has an explicit classification.**
- [ ] **Step 6: Commit `chore: inventory Unity third-party dependencies`.**

### Task 5: Create a static baseline system audit

**Files:**
- Create: `config/baseline/system-anchors.json`
- Create: `tools/foundation/baseline_audit.py`
- Create: `tools/foundation/tests/test_baseline_audit.py`
- Create: `docs/baseline/static-inventory.json`
- Create: `docs/baseline/static-inventory.md`

**Interfaces:**
- Produces: `SystemFinding(system: str, status: str, anchors_found: list[str], anchors_missing: list[str])`.
- Produces: `audit_systems(repo_root: Path, config_path: Path) -> list[SystemFinding]`.

- [ ] **Step 1: Write tests proving present anchors => `PRESENT`, a missing symbol => `UNRESOLVED`, and static presence is never upgraded to runtime-complete.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_baseline_audit -v`; expected FAIL.**
- [ ] **Step 3: Configure anchors for:**
  - Battle: `client/Assets/Scripts/Battle/BattleManager.cs`, `client/Assets/Scenes/Battle.unity`
  - Summon: `client/Assets/Scripts/Summon/SummonManager.cs`, `client/Assets/Scenes/Summon.unity`
  - Campaign: `client/Assets/Scripts/Campaign/LevelData.cs`
  - AFK: `client/Assets/Scripts/AfkRewards/KalineTreeManager.cs`, `AfkReward.cs`
  - Fusion: `client/Assets/Scripts/Ascension/AscensionManager.cs`, `client/Assets/Scenes/Ascension.unity`
  - Level/equipment: `client/Assets/Scripts/UnitDetail/UnitDetail.cs`, `UIEquipmentListElement.cs`
  - Backend: `client/Assets/Scripts/BackendConnection/SocketConnection.cs`, `gateway.proto`
- [ ] **Step 4: Generate reports with `python3 -m tools.foundation.baseline_audit --repo . --config config/baseline/system-anchors.json --json docs/baseline/static-inventory.json --markdown docs/baseline/static-inventory.md`.**
- [ ] **Step 5: Verify reports contain evidence classifications only plus the exact candidate SHA.**
- [ ] **Step 6: Commit `test: add static gameplay baseline audit`.**

### Task 6: Add repeatable foundation checks to Make and CI

**Files:**
- Modify: `Makefile`
- Create: `.github/workflows/nexus-foundation.yml`
- Create: `tools/foundation/tests/test_cli_contracts.py`

**Interfaces:**
- Produces Make targets `foundation-test`, `foundation-audit`, and `foundation-check`.

- [ ] **Step 1: Write tests asserting every audit has `--help`, invalid pins return non-zero, and inventory mode never hides known blockers.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_cli_contracts -v`; expected FAIL until CLI contracts are complete.**
- [ ] **Step 3: Add Make targets: `foundation-test` runs all foundation unit tests; `foundation-audit` runs provenance/dependency/static audits; `foundation-check` runs both.**
- [ ] **Step 4: Add GitHub Actions using Python 3.12 and `make foundation-check`; preserve the upstream format workflow rather than replacing it.**
- [ ] **Step 5: Run `make foundation-check`; expected PASS while known licensed-asset blockers remain explicitly reported.**
- [ ] **Step 6: Commit `ci: add Nexus foundation verification`.**

### Task 7: Probe the pinned backend baseline

**Files:**
- Create: `tools/foundation/probe_result.py`
- Create: `tools/foundation/backend_probe.py`
- Create: `tools/foundation/tests/test_backend_probe.py`
- Create/update: `docs/baseline/backend-runtime.md`
- Modify: `.gitignore` to ignore `artifacts/foundation/`
- Runtime output: `artifacts/foundation/backend/` (ignored except curated summary)

**Interfaces:**
- Produces shared `ProbeResult(status: Literal["PASS", "FAIL", "BLOCKED_DEP"], command: list[str], reason: str, artifact: str | None)`.
- Produces `probe_backend(dest: Path) -> list[ProbeResult]`.

- [ ] **Step 1: Write tests: missing `devenv` => `BLOCKED_DEP`; wrong backend SHA => `FAIL`; successful stub command => `PASS`.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_backend_probe -v`; expected FAIL.**
- [ ] **Step 3: Implement probe of exact checkout, Nix/devenv, Elixir/Mix, protobuf, and PostgreSQL without privileged auto-install.**
- [ ] **Step 4: When prerequisites exist, run compile/tests from the pinned backend and capture stdout/stderr under `artifacts/foundation/backend/`; genuine test failure => `FAIL`.**
- [ ] **Step 5: Run `python3 -m tools.foundation.backend_probe --backend .nexus/deps/mirra_backend --output artifacts/foundation/backend`.**
- [ ] **Step 6: Add `artifacts/foundation/` to `.gitignore`.**
- [ ] **Step 7: Curate exact-SHA outcome into `docs/baseline/backend-runtime.md`.**
- [ ] **Step 8: Record backend probe evidence in Brain at the exact candidate SHA.**
- [ ] **Step 9: Commit `test: probe Mirra backend baseline`.**

### Task 8: Probe Unity import/compile and current playable seams

**Files:**
- Create: `tools/foundation/unity_probe.py`
- Create: `tools/foundation/tests/test_unity_probe.py`
- Create/update: `docs/baseline/unity-runtime.md`
- Runtime output: `artifacts/foundation/unity/` (ignored except curated summary)

**Interfaces:**
- Consumes: Unity executable, exact `2021.3.26f1` project, dependency findings, `client/`.
- Produces: `probe_unity(project: Path, output: Path) -> list[ProbeResult]` using Task 7's status contract.

- [ ] **Step 1: Write tests for wrong Unity version, absent executable, missing required licensed asset, non-zero Unity exit, and compiler-error log signature even with exit 0.**
- [ ] **Step 2: Run `python3 -m unittest tools.foundation.tests.test_unity_probe -v`; expected FAIL.**
- [ ] **Step 3: Implement exact-version detection, dependency readiness check, batchmode import/compile, log capture, and key-scene enumeration.**
- [ ] **Step 4: Require scenes `Overworld`, `Battle`, `Summon`, `Ascension`, `KalineTree`, and `UnitDetail` to be reported individually as PRESENT/MISSING.**
- [ ] **Step 5: Run `python3 -m tools.foundation.unity_probe --project client --output artifacts/foundation/unity`; expected PASS or explicit `BLOCKED_DEP`, never proprietary auto-download.**
- [ ] **Step 6: If import succeeds, execute focused smoke paths: Overworld boot → Summon → Campaign/Battle → result → AFK rewards → Ascension/Fusion → Unit leveling/equipment.**
- [ ] **Step 7: Separate OBSERVED_RUNTIME from STATIC_ONLY findings in `docs/baseline/unity-runtime.md`.**
- [ ] **Step 8: Record Unity probe evidence in Brain at the exact candidate SHA.**
- [ ] **Step 9: Commit `test: certify Unity baseline`.**

### Task 9: Create isolated Game #2 Brain mission and measured backlog

**Files:**
- Create: `config/brain/mission.json`
- Create: `docs/baseline/foundation-gap-analysis.md`
- Create: `docs/roadmap/initial-transformation-backlog.md`
- Operational state: Brain objectives under a new `NEXUS-IDLE-RPG` root only.

**Interfaces:**
- Consumes: Tasks 2–8 reports and exact candidate SHA.
- Produces: `NEXUS-IDLE-RPG` mission tree plus backlog derived from measured gaps.

- [ ] **Step 1: Inspect live Brain immediately before mutation; confirm no duplicate Nexus Idle mission/tasks/leases exist.**
- [ ] **Step 2: Write `config/brain/mission.json` with `mission_id: NEXUS-IDLE-RPG`, title, and objectives `IDLE-FOUNDATION`, `IDLE-CLIENT`, `IDLE-BACKEND`, `IDLE-BATTLE`, `IDLE-PROGRESSION`, `IDLE-PRESENTATION`, `IDLE-CERTIFICATION`.**
- [ ] **Step 3: Run `/home/ubuntu/logres/bin/logres-mission init --config config/brain/mission.json`; expected idempotent mission load without modifying `LOGRES-RECONSTRUCTION`.**
- [ ] **Step 4: Run `/home/ubuntu/logres/bin/logres-mission tree NEXUS-IDLE-RPG --json`; assert all seven child objectives and parent IDs are correct.**
- [ ] **Step 5: Build `foundation-gap-analysis.md`; each row states current behavior, evidence/SHA, target behavior, dependency, and implementation-vs-external blocker.**
- [ ] **Step 6: Build backlog in playable order: account/boot → roster → five-hero formation → campaign → auto battle/energy/ultimates → victory/rewards → idle claim → summon/duplicate progression → level sync/ascension → equipment → tower/arena/guild/events → anime presentation polish.**
- [ ] **Step 7: Run `/home/ubuntu/logres/bin/logres-mission gaps`; expected remaining gaps correspond to intentional backlog work.**
- [ ] **Step 8: Run `make foundation-check`; expected PASS.**
- [ ] **Step 9: Verify `git merge-base --is-ancestor 116227e448b8ba375fb4aef80db6dafa33232909 HEAD`, backend pin `03ce828...`, and clean `git status --short`.**
- [ ] **Step 10: Record exact-SHA foundation completion evidence in Brain.**
- [ ] **Step 11: Commit `docs: publish measured idle RPG transformation backlog`.**

## Final Completion Gate

Foundation is complete only when Lambda history is preserved, integration/provenance/backend pins are verified, dependency and static audits are reproducible, CI passes, runtime probes have PASS evidence or genuine explicit blockers, Game #2 has isolated Brain state, and the transformation backlog comes from measured evidence. Missing Unity licensing/Asset Store dependencies may block runtime certification but must not block independent provenance, audit, backend, CI, or backlog work.
