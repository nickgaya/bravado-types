import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, NoReturn, Optional, Sequence, Tuple

from bravado.client import SwaggerClient

from bravado_types import generate_module
from bravado_types.config import (
    DEFAULT_ARRAY_TYPES,
    DEFAULT_CLIENT_TYPE_FORMAT,
    DEFAULT_MODEL_INHERITANCE,
    DEFAULT_MODEL_TYPE_FORMAT,
    DEFAULT_OPERATION_TYPE_FORMAT,
    DEFAULT_RESOURCE_TYPE_FORMAT,
    DEFAULT_RESPONSE_TYPES,
    ArrayTypes,
    Config,
    CustomFormats,
    ResponseTypes,
)


class _ArgumentParser(ArgumentParser):
    """
    ArgumentParser subclass with configurable error handling.
    :param exit: If false, raise RuntimeError instead of calling sys.exit() in
        case of errors.
    """
    def __init__(self, *args, exit: bool = True, **kwargs) -> None:
        self._exit = exit
        return super().__init__(*args, **kwargs)

    def error(self, message: str) -> NoReturn:
        if self._exit:
            super().error(message)
        else:
            raise RuntimeError(message)


def main(args: Optional[Sequence[str]] = None, exit: bool = True) -> None:
    """CLI entry point"""
    parser = _ArgumentParser(
        prog='bravado-types', exit=exit,
        description="Create a module and stub file for Bravado classes "
        "generated from a Swagger schema.")

    parser.add_argument(
        "--url",
        required=True,
        help="Schema url or path",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Schema name. Should be a valid Python identifier.",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path of generated module file. Must end with '.py'.",
    )

    parser.add_argument(
        "--client-type-format",
        default=None,
        help="Format string for generated client type. "
        f"Default {DEFAULT_CLIENT_TYPE_FORMAT!r}",
    )
    parser.add_argument(
        "--resource-type-format",
        default=None,
        help="Format string for generated resource types. "
        f"Default {DEFAULT_RESOURCE_TYPE_FORMAT!r}",
    )
    parser.add_argument(
        "--operation-type-format",
        default=None,
        help="Format string for generated operation types. "
        f"Default {DEFAULT_OPERATION_TYPE_FORMAT!r}",
    )
    parser.add_argument(
        "--model-type-format",
        default=None,
        help="Format string for generated model types. "
        f"Default {DEFAULT_MODEL_TYPE_FORMAT!r}",
    )

    parser.add_argument(
        "--array-types",
        choices=[at.value for at in ArrayTypes],
        default=None,
        help="Option for how array types should be represented."
        f"Default {DEFAULT_ARRAY_TYPES.value!r}"
    )

    parser.add_argument(
        "--response-types",
        choices=[rt.value for rt in ResponseTypes],
        default=None,
        help="Option for how operation response types should be represented."
        f"Default {DEFAULT_RESPONSE_TYPES.value!r}",
    )

    mi_group = parser.add_mutually_exclusive_group()
    mi_group.add_argument(
        "--model-inheritance",
        action='store_true',
        default=None,
        help="Enable model inheritance. The model type hierarchy will reflect "
        "model inheritance relationships as expressed by the allOf schema "
        "property."
        f"{ ' Enabled by default.' if DEFAULT_MODEL_INHERITANCE else ''}"
    )
    mi_group.add_argument(
        "--no-model-inheritance",
        action='store_false',
        dest='model_inheritance',
        default=None,
        help="Disable model inheritance.  Model types will only inherit from "
        "bravado_core.model.Model."
        f"{ '' if DEFAULT_MODEL_INHERITANCE else ' Enabled by default.'}"
    )

    parser.add_argument(
        "--custom-format",
        action='append',
        default=[],
        help="Type definition for custom format, given in the format "
        "<schema_type>:<schema_format>:<python_type>",
    )
    parser.add_argument(
        "--custom-format-package",
        action='append',
        default=[],
        help="Package to import for custom formats",
    )

    parser.add_argument(
        "--custom-templates-dir",
        default=None,
        help="Directory containing custom Mako templates.",
    )

    ns = parser.parse_args(args)

    url = _normalize_url(ns.url)
    client = SwaggerClient.from_url(url)

    array_types = ArrayTypes(ns.array_types) if ns.array_types else None
    response_types = (ResponseTypes(ns.response_types) if ns.response_types
                      else None)

    custom_formats = _custom_formats(ns.custom_format,
                                     ns.custom_format_package)

    config = Config(
        name=ns.name,
        path=ns.path,
        client_type_format=ns.client_type_format,
        resource_type_format=ns.resource_type_format,
        operation_type_format=ns.operation_type_format,
        model_type_format=ns.model_type_format,
        array_types=array_types,
        response_types=response_types,
        model_inheritance=ns.model_inheritance,
        custom_formats=custom_formats,
        custom_templates_dir=ns.custom_templates_dir,
    )

    generate_module(client, config,
                    _cli_args=sys.argv[1:] if args is None else args)


def _normalize_url(url_or_path: str) -> str:
    """
    :param url_or_path: A string containing a URL or a local filesystem path
    :return: A URL with scheme
    """
    if ":" in url_or_path:
        return url_or_path
    else:
        path = Path(url_or_path)
        return path.resolve().as_uri()


def _custom_formats(custom_formats: Sequence[str],
                    custom_format_packages: Sequence[str]) -> CustomFormats:
    format_dict: Dict[Tuple[str, str], str] = {}
    for custom_format in custom_formats:
        schema_type, schema_format, python_type = custom_format.split(':', 2)
        format_dict[schema_type, schema_format] = python_type
    return CustomFormats(format_dict, custom_format_packages)


if __name__ == "__main__":
    main()
