# ElevenID platform

Installation, deployment, release distribution and product lifecycle management.

This repository is the new platform entry point, beginning with the existing
signed installer bootstrap and independent artifact verification tools extracted
from [ElevenID/marty-ui](https://github.com/ElevenID/marty-ui).

**The trusted release producer and download URLs still belong to
`ElevenID/marty-ui`.** The bootstrap is byte-for-byte identical to source commit
[`9e098423`](https://github.com/ElevenID/marty-ui/commit/9e098423b5d98bc1bb50147f6cf1412973256144).
Its repository identity, signing workflows, pinned verifier binaries, release
admission checks and immutable artifact digests are preserved. Moving this
consumer does not change who is allowed to sign or publish a release.

## Installer entry point

Inspect the available options locally:

```sh
sh install.sh --help
```

The existing supported bootstrap target is Linux amd64, using a regular non-root
account with no-new-privileges and an already-running, same-user rootless Docker
daemon. On that prepared host, the limited host check is:

```sh
/usr/bin/setpriv --no-new-privs -- sh /absolute/platform/install.sh --check-host
```

That check makes no release downloads and creates no installation. It checks
bootstrap prerequisites and rootless connectivity; Compose, resources, release
availability and application readiness are separate gates. Normal installation
still requires an existing signed admission. An explicitly selected nightly
candidate remains unqualified and does not acquire Ready status.

The bootstrap downloads and verifies the native deployment operator and its
release metadata. It does not clone or build the application source. The
selected operator owns provisioning and retained installation state, including
managed OpenBao, TLS, external OIDC and lifecycle operations. Its implementation
and producer workflows remain in the source repository during this phase.

The [external OIDC](docs/installer-external-oidc.md) and
[application settings](docs/installer-application-settings.md) references point
to the matching source revision until those operator contracts are extracted.

## Artifact consumers

| Entry point | Responsibility | Result boundary |
| --- | --- | --- |
| `scripts/check_product_artifact_manifest.py` | Validate the existing product descriptor schema and immutable artifact references | Structural validity only |
| `scripts/verify_product_candidate.py` | Check bounded tar contents, checksums, product identity and exact source/run/attempt | Payload verification only |
| `scripts/verify_product_registry.py` | Check digest-linked OCI manifests, SPDX inventory and BuildKit provenance | Requires separate signed producer verification |
| `scripts/verify_product_attestations.py` | Bind already verified certificates and subjects to the exact candidate | Caller must first run the constrained cryptographic verifier |
| `scripts/product_evidence_intake.py` | Bind a verifier report to the exact candidate | Pending authenticated promotion |
| `scripts/authenticate_product_verification.py` | Authenticate the successful producer/verifier runs, artifacts and signed reports through `gh` | Pending runtime qualification |
| `scripts/verify_installer_provenance.py` | Verify a locally staged installer subject using caller-authenticated verifier binaries | No installation or release authorization |

The command-line consumers expose `--help`. Descriptor validation needs
`jsonschema`; the other imported Python tools use the standard library. Online
report authentication additionally needs a trusted `gh` executable and read
access to the named public workflow artifacts. The local installer verifier
requires absolute paths to independently authenticated `gh` and, when used,
`cosign` executables.

## Development

Python 3.11 or newer is required. Run the independent checks from this checkout:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
sh -n install.sh
```

Linux bootstrap tests use a POSIX shell, core utilities, `jq` and `setpriv` where
available. Platform/process-specific tests skip when their real preconditions
are unavailable. Test downloads, Docker observations and signature responses
are synthetic; the suite does not deploy a stack or qualify a live release.
CI checks out only this repository and has read-only permissions.

## Migration status

This first extraction provides the bootstrap and artifact-consumer boundary.
Native operator compilation, product publication, signed channel promotion,
deployment catalogs, Helm charts, fresh-install qualification, upgrade,
rollback and recovery remain with their existing owners until their independent
replacement gates pass. The current v1 package/descriptor contracts are kept;
the later cross-repository aggregate manifest must add explicit installer and
component compatibility constraints without changing existing provenance.

See the [extraction record](docs/extraction.md),
[ownership and follow-up work](docs/ownership.md), and
[hashed source map](migration/source-map.json). Application development remains
in `marty-ui`; the public website lives in `website`, and the separate Canvas
integration lives in `canvas-integration`.

## License and origin

AGPL-3.0-only. [LICENSE](LICENSE) is copied unchanged from the source repository.
Original authorship and source-history links are retained in
[ORIGIN.md](ORIGIN.md) and the source map.
