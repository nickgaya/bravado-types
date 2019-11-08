import os.path
from argparse import ArgumentParser
from typing import Optional, Sequence

from bravado.client import SwaggerClient

from bravado_types import generate_module
from bravado_types.render import (
    DEFAULT_ARRAY_TYPES,
    DEFAULT_CLIENT_TYPE_FORMAT,
    DEFAULT_MODEL_TYPE_FORMAT,
    DEFAULT_OPERATION_TYPE_FORMAT,
    DEFAULT_RESOURCE_TYPE_FORMAT,
    DEFAULT_RESPONSE_TYPES,
    ArrayTypes,
    RenderConfig,
    ResponseTypes,
)


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = ArgumentParser(description="Create a module and stub file for "
                            "Bravado classes generated from a Swagger schema.")

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
        help="Path of generated " "module file. Must end with '.py'.",
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
        help="Option for how operation response types should be annotated."
        "A value of 'success' indicates that response types should be a union "
        "of defined response types for 2xx status codes. A value of "
        "'all' indicates that response types should be a union of all "
        "documented response types. A value of 'any' indicates that all "
        "operations should be annotated as returning Any. "
        f"Default {DEFAULT_RESPONSE_TYPES.value!r}",
    )

    parser.add_argument(
        "--custom-templates-dir",
        default=None,
        help="Directory containing custom Mako templates.",
    )

    ns = parser.parse_args(args)

    url = _normalize_url(ns.url)
    client = SwaggerClient.from_url(url)

    render_config = RenderConfig(
        name=ns.name,
        path=ns.path,
        client_type_format=ns.client_type_format,
        resource_type_format=ns.resource_type_format,
        operation_type_format=ns.operation_type_format,
        model_type_format=ns.model_type_format,
        array_types=ns.array_types,
        response_types=ns.response_types,
        custom_templates_dir=ns.custom_templates_dir,
    )

    generate_module(client, render_config)


def _normalize_url(url_or_path: str) -> str:
    """
    :param url_or_path: A string containing a URL or a local filesystem path
    :return: A URL with scheme
    """
    if ":" in url_or_path:
        return url_or_path
    else:
        path = os.path.abspath(url_or_path)
        return f"file://{path}"


if __name__ == "__main__":
    main()
