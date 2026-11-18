# First platform extraction

## Scope and source

The source snapshot is
[`ElevenID/marty-ui@9e098423b5d98bc1bb50147f6cf1412973256144`](https://github.com/ElevenID/marty-ui/tree/9e098423b5d98bc1bb50147f6cf1412973256144).
The target is a source-independent installer entry point and artifact consumer.
No existing source file is deleted, renamed or redirected by this PR.

`install.sh` is already a self-contained bootstrap for immutable signed
artifacts. It does not depend on repository-relative runtime files or a complete
application checkout. It is copied without a byte change, including the
complete-download terminator, Linux/rootless process checks, isolated Docker
configuration, pinned verifier downloads, admission/channel checks, certificate
identity, source/run/attempt checks and operator handoff. The trusted producer
repository, numeric public repository identifier and release URLs stay intact.

Seven existing Python consumer modules, their two schemas, and the original
license are copied. The only consumer wiring change removes a transitive
dependency on the product build planner: `product_evidence_intake.py` now calls
`product_package_identity.py`. That small module contains the existing package
identity and immutable-image validation from `compose_product_packages.py`,
using the same product/version/source constants from `product_package_plan.py`.
It neither builds packages nor renders a deployment.

The source map lists byte-identical and adapted paths separately. Producer
identity is not replaced with this destination repository's name: that would
invalidate the meaning of the currently signed evidence.

## Independent validation

Local extraction validation completed with Python 3.12:

| Check | Observed result |
| --- | --- |
| Imported consumer/bootstrap suite with portable test data | 256 passed, 3 skipped |
| Shell syntax check | Passed |
| `install.sh` comparison with pinned source | Byte-identical |
| Original server producer archive consumed by extracted verifier | Passed: 47 files, 36 runtime files |
| Original console producer archive consumed by extracted verifier | Passed: 10 files, no server runtime files |

The skipped tests require a process without no-new-privileges, or a root
process. The available test process already had no-new-privileges and was
non-root. The real non-root shell tests still exercised isolated Docker config,
same-user socket pinning, inherited-environment exclusion and cleanup using
synthetic Docker/download responses.

The original producer compatibility experiment ran the original
`product_package_plan.py` against the pinned source tree, with explicitly
synthetic image receipts, then passed the resulting archives to the extracted
consumer. Only the summary is committed in
[`migration/product-builder-compatibility.json`](../migration/product-builder-compatibility.json).
The experiment's runtime assets and source-dependent builder are not copied into
this repository. The committed fixture builder creates small synthetic archives
for repeatable offline tests. Those fixtures and mock certificate responses are
not authentic signed release evidence.

The original producer-dependent guide-generation test stays in `marty-ui`.
Its generator is not part of this slice. The remaining Linux bootstrap tests
are carried here. CI uses Python 3.11 on Ubuntu, checks out only `platform`,
executes the tests, and performs no release publication or deployment.

## Gates still required

1. Authenticate a live selected release through this checkout and qualify its
   complete fresh install on the existing isolated environment.
2. Extract and build the native operator with its reviewed crate dependencies,
   installer data contracts and lifecycle tests. Keep application services,
   protocol implementations and the Canvas worker with their owners.
3. Version the cross-repository aggregate release manifest and compatibility
   contract, including minimum installer version. Preserve each component's
   original producer workflow/run/attempt and signature evidence.
4. Qualify independent operator packaging, signing, release admission and
   channel promotion before changing any pinned trust identity or release URL.
5. Qualify existing-install upgrade, rollback, backup and recovery, rootless
   reboot behavior, OpenBao, TLS, external OIDC and selected Kubernetes paths.
6. Retire source copies only after the destination becomes the qualified owner
   and active source PRs have been reconciled.

No live cryptographic verification, new release, production deployment, resource
expansion or installed-state migration is claimed by the local test results.
