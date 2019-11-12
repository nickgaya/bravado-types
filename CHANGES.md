# Changelog

## 0.3.0

- Specify minimum versions of bravado and bravado-core in setup.py
- Remove unneccessary quoting of forward references in pyi template
- Fix handling of `--array-types` and `--return-types` CLI flags
- Change `ReturnTypes.union` to `ReturnTypes.all`
- Fix attribute error in template when `config.return_types` is set to `all`
- Add `--model-inheritance` / `--no-model-inheritance` flags to CLI
- Fix model inheritance template bug
- Add package classifiers

## 0.2.0

- Add _request_options to operation call parameters
- Add informational header to generated files
- Define `bravado-types` CLI entry point
- Use enum class for return_types config parameter
- Refactor type representation in data model
- Add configuration parameter for rendering array types
- Fix template bug when schema has no models or resources
- Create runtime subclass of SwaggerClient
- Make default client and model type names more consistent
- Use `typing.Mapping` instead of `typing.Dict` in generated stub file
- Remove Black postprocessor

## 0.1.0

- Initial release. This project is still under development and may undergo
backward-incompatible changes until version 1.0 is released.
