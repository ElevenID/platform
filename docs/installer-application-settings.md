# Application settings input

The bootstrap forwards `--settings-file` as one opaque argument to the
authenticated native deployment operator. Typed validation, secret-file custody
and retained installation records remain owned by that operator.

Use the [application settings guide at the extracted source revision](https://github.com/ElevenID/marty-ui/blob/9e098423b5d98bc1bb50147f6cf1412973256144/docs/installer-application-settings.md)
for accepted fields and combinations. Supply private configuration outside this
checkout and use the contract supported by the selected operator release.

This extraction does not expand configuration permissions, change deployment
profiles, migrate installed state, or move the Canvas implementation into the
platform repository.
