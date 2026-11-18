# External OIDC installer input

The bootstrap forwards `--external-oidc-file` unchanged to the authenticated
native deployment operator. That operator and its exact typed input contract
remain with the current release producer during this extraction.

Use the [external OIDC guide at the extracted source revision](https://github.com/ElevenID/marty-ui/blob/9e098423b5d98bc1bb50147f6cf1412973256144/docs/installer-external-oidc.md)
for provider prerequisites, private configuration, optional scopes and client
authentication, local-session behavior, and qualification limits. Match those
capabilities to the actual selected operator release.

The independent external-OIDC option retains managed OpenBao. It is mutually
exclusive with `--foundation-file`; provider client registration and browser
login/callback qualification remain separate operator tasks. This repository
does not provision an identity provider or claim a live provider qualification.
