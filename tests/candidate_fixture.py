"""Portable, synthetic v1 candidates; no container payload or valid signatures.

These fixtures exercise consumer parsing. Extraction validation also compares
against archives emitted by the pinned original producer (see docs/extraction.md).
"""
import hashlib
import io
import json
import tarfile
from pathlib import Path


def write_candidate(root: Path, product: str) -> tuple[Path, Path, Path]:
    roles = ("keycloak", "migrations", "openbao-didcomm", "services") if product == "marty-server" else ("ui",)
    version = "0.1.0"
    tag = ("server-v" if product == "marty-server" else "console-v") + version
    runtime = ({f"fixture-{index}.txt": b"synthetic runtime fixture\n" for index in range(36)}
               if product == "marty-server" else {})
    plan = {
        "schema": "marty.product-build-plan/v1", "repository": "ElevenID/marty-ui",
        "source_sha": "a" * 40, "product": product, "version": version, "tag": tag,
        "qualification": "unqualified",
        "images": [{"role": role, "image": f"ghcr.io/elevenid/{product}/{role}"} for role in roles],
        "runtime_files": [{"path": path, "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
                           "source_sha256": "sha256:" + hashlib.sha256(data).hexdigest()}
                          for path, data in runtime.items()],
    }
    package = {
        "schema": "marty.product-package/v1", "product": product, "version": version, "tag": tag,
        "source": {"repository": "ElevenID/marty-ui", "commit": "a" * 40},
        "api": {"http": "v1", "mip": "0.5.0"}, "platforms": ["linux/amd64"],
        "images": [{"role": role, "uri": f"ghcr.io/elevenid/{product}/{role}",
                    "digest": "sha256:" + "e" * 64, "platform": "linux/amd64"} for role in roles],
        "build_plan_sha256": "sha256:" + hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "producer": {"workflow": ".github/workflows/product-packages.yml", "run_id": "123", "run_attempt": "2"},
        "support_state": "experimental", "qualification": "unqualified",
    }
    package_bytes = (json.dumps(package, sort_keys=True, indent=2) + "\n").encode()
    files = {"product-package.json": package_bytes,
             "build-plan.json": (json.dumps(plan, sort_keys=True, indent=2) + "\n").encode(),
             **{"runtime/" + path: data for path, data in runtime.items()}}
    if product == "marty-console":
        files["docker-compose.console.yml"] = b"# Synthetic fixture; never deploy.\n"
    files["SHA256SUMS"] = "".join(hashlib.sha256(data).hexdigest() + "  " + path + "\n"
                                  for path, data in sorted(files.items())).encode()
    archive = root / "product-package.tar.gz"
    with tarfile.open(archive, "w:gz", format=tarfile.PAX_FORMAT) as bundle:
        if runtime:
            directory = tarfile.TarInfo("runtime")
            directory.type = tarfile.DIRTYPE
            directory.mode = 0o755
            bundle.addfile(directory)
        for name, data in sorted(files.items()):
            member = tarfile.TarInfo(name)
            member.size, member.mode = len(data), 0o644
            bundle.addfile(member, io.BytesIO(data))
    checksum = root / "product-package.tar.gz.sha256"
    checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + "  product-package.tar.gz\n")
    package_path = root / "product-package.json"
    package_path.write_bytes(package_bytes)
    return archive, checksum, package_path
