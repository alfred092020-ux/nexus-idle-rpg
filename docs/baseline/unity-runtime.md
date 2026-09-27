# Unity Runtime Baseline

Required editor: `2021.3.26f1`
Overall: `BLOCKED_DEP`

## STATIC_ONLY

- PASS: /home/ubuntu/tools/unity/2021.3.26f1/Editor/Unity -version: Unity editor version 2021.3.26f1
- PASS: project-version: project Unity version 2021.3.26f1
- PASS: scene Overworld: Overworld: PRESENT
- PASS: scene Battle: Battle: PRESENT
- PASS: scene Summon: Summon: PRESENT
- PASS: scene Ascension: Ascension: PRESENT
- PASS: scene KalineTree: KalineTree: PRESENT
- PASS: scene UnitDetail: UnitDetail: PRESENT
- BLOCKED_DEP: dependency com.coffee.ui-particle: com.coffee.ui-particle: license/redistribution review unresolved (UPSTREAM_LICENSE_REVIEW)
- BLOCKED_DEP: dependency com.github-glitchenzo.nugetforunity: com.github-glitchenzo.nugetforunity: license/redistribution review unresolved (UPSTREAM_LICENSE_REVIEW)
- BLOCKED_DEP: dependency xyz.candycoded.hapticfeedback: xyz.candycoded.hapticfeedback: license/redistribution review unresolved (UPSTREAM_LICENSE_REVIEW)
- BLOCKED_DEP: dependency RPG & MMO UI 6: RPG & MMO UI 6: required dependency missing at client/Assets/ThirdParty/RPG & MMO UI 6
- BLOCKED_DEP: dependency Map Maker: Map Maker: required dependency missing at client/Assets/ThirdParty/Map Maker
- BLOCKED_DEP: dependency RPG inventory icons: RPG inventory icons: required dependency missing at client/Assets/ThirdParty/RPG inventory icons
- BLOCKED_DEP: dependency Basic RPG Icons: Basic RPG Icons: required dependency missing at client/Assets/ThirdParty/Basic RPG Icons
- BLOCKED_DEP: dependency Resource Vector Graphics: Resource Vector Graphics: license/redistribution review unresolved (ASSET_STORE_LICENSE_REVIEW)
- BLOCKED_DEP: dependency DOTween: DOTween: license/redistribution review unresolved (ASSET_STORE_LICENSE_REVIEW)
- BLOCKED_DEP: dependency Gold Mining Game: Gold Mining Game: required dependency missing at client/Assets/ThirdParty/Gold Mining Game
- BLOCKED_DEP: dependency UX Flat Icons: UX Flat Icons: required dependency missing at client/Assets/ThirdParty/UX Flat Icons

## OBSERVED_RUNTIME

- BLOCKED_DEP: direct Unity 2021.3.26f1 batch import was attempted outside the guarded preflight probe. The editor launched and licensing client connected, but import stopped before project load because no active Unity Editor license was installed. Evidence: `artifacts/foundation/unity-direct/import.log` (ignored runtime artifact).
- No C# compiler result is claimed because the editor exited at the licensing gate.

The probe never downloads proprietary or Asset Store dependencies automatically.
