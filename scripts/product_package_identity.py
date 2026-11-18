"""Validate existing v1 product package identities without producer source.

Extracted from marty-ui product_package_plan.py and compose_product_packages.py.
This structural check does not authenticate signatures or qualify a release.
"""
from __future__ import annotations

import re

PRODUCTS = {
    "marty-server": ("server-v", {"services", "migrations", "openbao-didcomm", "keycloak"}),
    "marty-console": ("console-v", {"ui"}),
}
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
SHA = re.compile(r"[0-9a-f]{40}")
PINNED_IMAGE = re.compile(r"[a-z0-9][a-z0-9:._/-]*@sha256:[0-9a-f]{64}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def package_images(package: dict) -> dict[str, str]:
    require(
        package.get("schema") == "marty.product-package/v1",
        "product package schema is invalid",
    )
    product = package.get("product")
    require(product in PRODUCTS, "product package identity is invalid")
    require(
        VERSION.fullmatch(str(package.get("version"))) is not None,
        "product version is invalid",
    )
    prefix, roles = PRODUCTS[product]
    require(
        package.get("tag") == prefix + package["version"],
        "product tag differs from its version",
    )
    source = package.get("source", {})
    require(
        source.get("repository") == "ElevenID/marty-ui"
        and SHA.fullmatch(str(source.get("commit"))) is not None,
        "product source is invalid",
    )
    require(
        package.get("api") == {"http": "v1", "mip": "0.5.0"},
        "product API contract is incompatible",
    )
    images = package.get("images", [])
    require(
        len(images) == len(roles) and {image.get("role") for image in images} == roles,
        "product image role set differs",
    )
    refs = {}
    for image in images:
        uri = "ghcr.io/elevenid/" + product + "/" + image["role"]
        require(
            image.get("uri") == uri and image.get("platform") == "linux/amd64",
            "product image identity differs",
        )
        ref = uri + "@" + str(image.get("digest"))
        require(
            PINNED_IMAGE.fullmatch(ref) is not None,
            "product image must be digest-pinned",
        )
        refs[image["role"]] = ref
    return refs
