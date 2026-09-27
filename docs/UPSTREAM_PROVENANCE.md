# Lambda Client Upstream Provenance

The Nexus Idle RPG foundation preserves the Git history of the public Lambda-Forge `afk_gacha_game` repository instead of flattening it into a source snapshot.

- Upstream: `https://github.com/Lambda-Forge/afk_gacha_game.git`
- Reviewed branch: `main`
- Reviewed commit: `116227e448b8ba375fb4aef80db6dafa33232909`
- Code license recorded for the reviewed upstream: Apache-2.0
- Unity editor baseline: `2021.3.26f1`
- Preserved vendor ref: `vendor/lambda-main`

The reviewed commit is immutable provenance. Movement of upstream `main` does not update this pin automatically; a pin change requires explicit review and new evidence.

The Apache-2.0 code classification does not automatically grant redistribution rights for graphics, audio, fonts, Unity Asset Store packages, or other third-party content. Those obligations are inventoried separately.

Verify from the repository root:

```bash
python3 -m tools.foundation.provenance --repo . --pin config/upstreams/lambda-client.json --ref HEAD
```
