# Ownership boundaries and next extractions

This is a responsibility review for the first platform slice, not an assertion
that every installer-related source file is ready to move. The imported paths
are explicitly allowlisted in `migration/source-map.json`.

| Source area | Responsibility | Destination decision |
| --- | --- | --- |
| `install.sh` | Signed artifact acquisition and native-operator bootstrap | Copied unchanged into platform now |
| Product payload, registry, attestation and report consumers | Verify immutable component artifacts and evidence | Copied into platform now |
| `verify_installer_provenance.py` | Verify private staged installer subjects | Copied unchanged into platform now |
| Product package/artifact schemas | Existing consumer contracts | Copied with existing schema identities |
| `product_package_plan.py`, `product_image_build.py`, `product-packages.yml` | Build application-owned product images and packages from source | Remain with application producer; only identity validation extracted |
| `rust/crates/deployment-catalog/` | Mixed deployment catalog, native operator and installer state/lifecycle | Review module and crate dependencies before a separate operator extraction |
| `rust/crates/acme-client/`, `selfhost-bundle/`, `selfhost-identity/`, `release-evidence/` | Installer-related shared libraries with product dependencies | Inspect consumers and package boundaries before transferring ownership |
| `installer_release.py`, `installer_promote.py`, `installer_channel.py`, publish/admission helpers | Installer release orchestration and trust policy | Next platform-owned candidate, with entire import closure and release qualification |
| Candidate/acceptance runner and VM tooling | Qualification orchestration and isolated environment policy | Platform candidate after active PR reconciliation; preserve automatic stop and resource limits |
| `deploy-config/host/`, selected installer Compose overlays | Host/TLS setup and deployment orchestration | Platform candidate after native operator/assets contract exists |
| `deploy-config/catalog/services.json`, runtime configs and container entrypoints | Product runtime definition | Consume application-owned versioned artifacts instead of transplanting services |
| `deploy/helm/marty/` | Deployment templates mixed with copied application/Keycloak runtime assets | Split orchestration from producer-owned assets; qualify chart before handoff |
| `deploy/k3s/`, `k8s/oracle/` | Environment-specific deployment recipes | Review maintained profiles and private operational assumptions before selection |
| `openbao/didcomm-authcrypt/backend/`, protocol JWE implementation | Service/protocol implementation | Stay with service owner; platform consumes signed images |
| `openbao/didcomm-authcrypt/cmd/selfhost-*`, `internal/openbaocontrol/` | Mixed custody/lifecycle helpers built in the plugin module | Explicit source/build boundary review; do not copy the entire OpenBao subtree |
| `manage-ui.sh`, development Compose and source-build helpers | Existing development and legacy workflow | Preserve current owner while development layout work continues |
| Canvas implementation, fixtures and producer | Independent integration | Keep `ElevenID/canvas-integration`; platform may consume a qualified artifact |
| Private commerce/subscriptions implementation and producer | Private component | Keep isolated; public platform only consumes its approved public contract |
| `SELFHOST_*` and deployment guides | Mixed product/operator instructions | Move only with the matching qualified implementation and corrected links |

## Active work to reconcile

These source PRs were active when the migration was inspected. The extraction
pins main; it does not imply approval or incorporation of their branches.

| Source PR | Overlap to revisit before the next slice |
| --- | --- |
| [#1968](https://github.com/ElevenID/marty-ui/pull/1968) | Installer startup acceptance and candidate rendezvous |
| [#1967](https://github.com/ElevenID/marty-ui/pull/1967) | Release ordering in `cd.yml` |
| [#1920](https://github.com/ElevenID/marty-ui/pull/1920) | Development Compose layout |
| [#1910](https://github.com/ElevenID/marty-ui/pull/1910) | Kubernetes chart, Canvas/OB3 and renewal tooling |
| [#1710](https://github.com/ElevenID/marty-ui/pull/1710) | Rootless VM qualification and rendezvous |
| [#1683](https://github.com/ElevenID/marty-ui/pull/1683) | Purge/diagnostics work with existing conflicts |
| [#1783](https://github.com/ElevenID/marty-ui/pull/1783) | Public verification website work; coordinate with `website`, not this platform slice |

Before removal of any source copy, refresh these PRs and record whether each
landed change belongs in platform, application, website or Canvas. Keep the
original release workflows operational until replacement workflows qualify.
