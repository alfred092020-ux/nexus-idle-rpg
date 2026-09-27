# Nexus Idle RPG Foundation Design

Date: 2026-09-26
Status: Design approved in chat; written-spec review pending
Repository: `alfred092020-ux/nexus-idle-rpg`
Target integration branch: `feat/idle-rpg-foundation`

## 1. Purpose

Create a clean, legally traceable foundation for Nexus Core's second game by preserving the full Git history of Lambda-Forge's open-source `afk_gacha_game`, establishing an isolated Game #2 workflow, and proving the existing project works before transforming it toward an original Girls' Connect-style idle gacha.

The project must remain independent from the Logres reconstruction. Logres code, evidence, task state, branches, device claims, and historical-reconstruction rules must not leak into this game unless deliberately reused as generic studio infrastructure.

## 2. Success Criteria

The foundation stage is successful when:

1. Lambda's upstream history is preserved intact in the Nexus repository.
2. `main` is not used as the development integration branch.
3. `feat/idle-rpg-foundation` is the canonical integration branch for Game #2.
4. Upstream provenance is pinned to exact source SHAs and documented.
5. The Unity client and required backend can be reproduced from documented steps.
6. Missing third-party assets and license boundaries are explicitly identified.
7. A baseline audit documents what Battle, Summon, Campaign, AFK Rewards, Fusion, Leveling, inventory/equipment, and backend/account flows actually do today.
8. Automated verification exists before feature transformation begins.
9. Game #2 receives its own Brain mission namespace, tasks, leases, workers, and verification evidence.
10. No proprietary Girls' Connect code, art, audio, characters, text, or assets are imported.
## 3. Upstream Sources and Provenance

Primary client upstream:
- Repository: `Lambda-Forge/afk_gacha_game`
- Upstream branch: `main`
- Baseline SHA observed during design: `116227e448b8ba375fb4aef80db6dafa33232909`
- Unity version: `2021.3.26f1`
- Code license: Apache License 2.0
- Graphics/music: separate Creative Commons attribution/share-alike terms per upstream README

Backend upstream:
- Repository: `lambdaclass/mirra_backend`
- Upstream branch: `main`
- Baseline SHA observed during design: `03ce82842a5d2d36f3a58396e7f22e0a43dfcb86`

The implementation plan must re-check both SHAs immediately before import. If either upstream moves, the imported SHA must be the exact reviewed commit, not an assumed latest state.

A provenance file will record source repository, exact commit, license, import date, and any subsequent upstream merges. Original license and attribution files must remain intact.

## 4. Repository and Branch Model

`alfred092020-ux/nexus-idle-rpg` is the Nexus-owned repository.

The Lambda client history will be imported without squashing or flattening. Locally, the original Lambda repository will remain configured as `upstream` so later comparison and selective upstream merges remain possible.

Development will not occur directly on `main`. The canonical Game #2 integration branch will be `feat/idle-rpg-foundation`.

Feature workers will use isolated branches/worktrees derived from the current integration HEAD. Each worker must hold a Brain lease before editing. Integration requires verification evidence at the exact candidate SHA.

The docs-only branch `docs/nexus-idle-foundation-spec-001` exists solely to review this architecture before implementation and is not the future integration root.
## 5. Dependency and Asset Policy

The open-source code and the game's assets are treated as separate legal surfaces.

The implementation must not assume every file referenced by upstream is redistributable. The upstream README requires several Unity Asset Store packages and TextMeshPro resources. Those dependencies must be classified as one of:

- already included and redistributable under the upstream license,
- free but separately licensed and installable from the publisher,
- paid/proprietary and requiring a Nexus-owned license,
- replaceable with an original/open alternative,
- unnecessary for the Nexus target and removable.

No worker may copy paid Asset Store content from another machine, archive, or project unless Nexus has a valid license for that asset. Missing proprietary dependencies should fail explicitly and be recorded rather than silently substituted.

For graphics and music already present upstream, attribution/share-alike obligations must be preserved until those assets are replaced. The long-term Nexus release should prefer original Nexus art/audio so the commercial product has a clean identity and simpler provenance.

## 6. Backend Boundary

The Mirra backend remains a separately tracked upstream dependency during the baseline stage. It will not be merged into the client repository merely for convenience.

The first audit must map:
- authentication/account flow,
- websocket/session lifecycle,
- user/profile state,
- summon requests and currency validation,
- inventory/unit persistence,
- campaign/battle state exchanged with the client,
- AFK reward calculation/storage,
- configuration and database dependencies.

After the baseline is proven, a separate architecture decision can choose between maintaining a Nexus fork of Mirra, replacing it with a Nexus backend, or extracting only the services actually needed. That decision is outside this foundation spec.
## 7. Baseline Audit Before Transformation

The first engineering milestone is preservation and measurement, not redesign.

The team must establish a reproducible baseline and inventory the current project by answering, with code references and runtime evidence:

- Which scenes are launchable and in what order?
- Which systems are client-authoritative versus backend-authoritative?
- Does Battle complete end-to-end and persist its result?
- Does Summon validate currency and return/persist the awarded unit?
- How are Campaign stages selected, started, won, and unlocked?
- How are AFK rewards accumulated, capped, claimed, and persisted?
- How does Fusion modify owned units and handle duplicates?
- How does Leveling spend resources and enforce caps?
- What inventory/equipment functionality exists versus being stubbed or unfinished?
- Which UI screens are functional, incomplete, or disconnected?
- Which tests, linters, CI jobs, and build scripts already exist?
- Which missing assets prevent a clean Unity import or runnable build?

Every claim about completeness must be based on repository evidence or a verified runtime path. Upstream milestone percentages are useful context, not proof that a feature is complete.

## 8. Brain and Autonomous-Studio Isolation

Game #2 receives a distinct project/mission namespace, rooted under a Nexus Idle mission rather than `LOGRES-RECONSTRUCTION`.

Tasks must carry a Game #2 lane/mission identity. Leases, worktrees, verification artifacts, candidate SHAs, regression signatures, and device claims must be attributable to this repository.

Generic studio infrastructure may be shared, including worker orchestration, verification runners, learned routing, recovery, and lawful tool building. Project facts must not be shared implicitly.

Resource scheduling should keep the two games from starving each other. Heavy full-E2E/performance lanes should be serialized or quota-controlled when they contend for the same VM resources. Physical Android testing remains exclusive and claim-based.
## 9. Product Transformation Target

The long-term game is an original Nexus idle gacha inspired by the structure and pacing of games such as Girls' Connect, not a copy of their protected expression.

The target gameplay direction after baseline certification is:
- five-hero teams with meaningful formation placement,
- front/back positioning where appropriate,
- defined combat roles such as tank, damage, control, and support,
- factions/elements and counter relationships,
- automatic basic combat with energy/ultimate skills,
- buffs, debuffs, crowd control, and damage-over-time effects,
- collectible authored heroes rather than anonymous random units,
- duplicate/shard-based ascension,
- level synchronization or equivalent roster catch-up,
- idle/offline rewards tied to campaign progress,
- campaign, tower/challenge, arena, guild/boss, and event-capable progression,
- summon banners, pity/guarantee rules, and transparent server-authoritative economy,
- original anime-style characters, UI, story, animation, VFX, and audio.

These are product-direction requirements, not permission to implement all of them during the foundation milestone. They guide which upstream systems are preserved, replaced, or extended.

## 10. Architecture Principles

Preserve working upstream seams before replacing them. New Nexus systems should have clear interfaces so combat, economy, persistence, presentation, and live-ops logic can be tested independently.

Server-authoritative state is preferred for anything economically valuable or competitively relevant: account inventory, currency spending, summons, progression rewards, and PvP outcomes. The client owns presentation, prediction where safe, and input orchestration.

Configuration that designers are expected to tune should be data-driven rather than buried in scene scripts. Hero definitions, skills, factions, progression curves, summon tables, stages, and reward tables should migrate toward validated data models as the project evolves.
## 11. Error Handling and Missing Dependencies

Baseline tooling must distinguish source defects from environment/setup defects. A failed build caused by an unavailable Asset Store package must be reported differently from a compile error in open-source code.

Required behavior:
- fail closed when a required dependency or license is unknown,
- print the exact missing package/file/tool and the action needed,
- never download paid or unverified assets automatically,
- keep secrets and credentials out of Git,
- make backend connection failures diagnosable without exposing secrets,
- record reproducible blockers in Brain with exact SHAs and logs/artifacts.

Where a dependency is optional, the project should degrade predictably or provide a documented development substitute. Any substitute used for testing must be visibly marked and must not be mistaken for production content.

## 12. Verification Strategy

Foundation verification follows an evidence ladder:

1. repository/provenance checks,
2. dependency inventory and license checks,
3. static compile/lint checks available without Unity runtime,
4. Unity project import/compile on the exact baseline SHA,
5. backend startup and health verification,
6. focused runtime tests for individual systems,
7. client-backend integration tests for summon/account/progression flows,
8. a playable smoke path through the currently implemented game loop,
9. exact-SHA Android build/device proof when the project reaches that stage.

A worker saying a feature works is not completion evidence. Each verified milestone must record the exact SHA, commands/tests, result, and relevant runtime artifact.

## 13. Non-Goals of the Foundation Stage

The foundation stage does not:
- recreate Girls' Connect assets, characters, story, UI, or proprietary source,
- promise that every Lambda feature is production-ready,
- redesign the entire backend before its existing behavior is measured,
- add monetization before core progression is verified,
- migrate Unity versions merely because a newer version exists,
- merge Game #2 task state into Logres,
- begin broad art replacement before the runnable baseline is understood.
## 14. Foundation Completion Criteria

The foundation implementation may be called complete only when all of the following are true:

- the reviewed Lambda commit is present with its original history,
- `upstream` points to the original Lambda repository in the working clone setup,
- `feat/idle-rpg-foundation` exists and is the Game #2 integration branch,
- provenance and license obligations are committed and readable,
- required third-party dependencies are enumerated with acquisition/license status,
- Mirra backend setup is pinned and reproducible,
- the client can be imported/compiled as far as legitimately available dependencies allow,
- the existing gameplay systems have a code/runtime audit with evidence,
- automated checks exist for the portions that can run headlessly,
- known blockers are explicit rather than hidden by stubs,
- Brain contains the Game #2 mission/task structure and verification evidence,
- a prioritized transformation backlog is derived from measured gaps rather than assumptions.

## 15. Decisions Fixed by This Spec

The following choices are deliberate and should not be revisited during implementation without new evidence:

1. Preserve Lambda history rather than snapshotting it.
2. Use `feat/idle-rpg-foundation` rather than `main` for integration.
3. Keep the backend separate during baseline certification.
4. Verify the upstream game before transforming it.
5. Keep open-source code provenance separate from third-party asset licensing.
6. Build an original Nexus product inspired by the genre, not a protected-expression clone.
7. Isolate Game #2 operational state from Logres while reusing generic autonomous-studio infrastructure.

Any change to these decisions requires a recorded architecture decision with the reason, affected SHAs, and migration impact.