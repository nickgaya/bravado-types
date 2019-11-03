"""Functions for mapping Swagger definitions to Python types."""

import warnings
from typing import Any, Dict

from bravado_core.schema import get_type_from_schema
from bravado_core.spec import Spec

from bravado_types.data_model import TypeDef

# Map of Swagger primitive types to Python types
SWAGGER_PRIMITIVE_TYPES = {
    'integer': 'int',
    'number': 'float',
    'string': 'str',
    'boolean': 'bool',
    'null': 'None',
}

# Map of Swagger types to maps of format names to Python types
SWAGGER_FORMATS = {
    'integer': {
        'int32': 'int',
        'int64': 'int',
    },
    'number': {
        'float': 'float',
        'double': 'float',
    },
    'string': {
        'byte': 'bytes',
        'date': 'datetime.date',
        'date-time': 'datetime.datetime',
        'password': 'str',
    },
}


def get_type(spec: Spec, schema: Dict[str, Any]) -> TypeDef:
    """
    Get the type of a schema within a Swagger spec.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeDef for the schema.
    """
    schema = spec.deref(schema)
    schema_type = get_type_from_schema(spec, schema)
    if schema_type == "array":
        typedef = _get_array_type(spec, schema)
    elif schema_type == "object":
        typedef = _get_object_type(spec, schema)
    elif schema_type in SWAGGER_PRIMITIVE_TYPES:
        typedef = _get_primitive_type(spec, schema)
    elif schema_type == "file":
        typedef = TypeDef("typing.Any")
    elif schema_type is None:
        typedef = TypeDef("typing.Any")
    else:
        warnings.warn(f"Unknown schema type: {schema_type!r}")
        typedef = TypeDef("typing.Any")

    if schema.get("x-nullable", False):
        typedef = typedef.wrap("typing.Optional[{}]")
    return typedef


def _get_array_type(spec: Spec, schema: Dict[str, Any]) -> TypeDef:
    """
    Get the type of an array schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeDef for the schema.
    """
    item_type = get_type(spec, schema["items"])
    return item_type.wrap("typing.Sequence[{}]")


def _get_object_type(spec: Spec, schema: Dict[str, Any]) -> TypeDef:
    """
    Get the type of an object schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeDef for the schema.
    """
    if "x-model" in schema:
        return TypeDef("{}", schema["x-model"])

    # Special case: allOf with a single item. This may be used to specify a
    # nullable ref, like this:
    #
    # x-nullable: true
    # allOf:
    #   - $ref: '#/definitions/Model'
    if ('allOf' in schema and len(schema['allOf']) == 1
            and 'properties' not in schema):
        return get_type(spec, schema['allOf'][0])

    return TypeDef("typing.Dict[str, typing.Any]")


def _get_primitive_type(spec: Spec, schema: Dict[str, Any]) -> TypeDef:
    """
    Get the type of a primitive schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeDef for the schema.
    """
    schema_type = schema["type"]
    if "format" in schema:
        schema_format = schema["format"]
        format_type = SWAGGER_FORMATS.get(schema_type, {}).get(schema_format)
        if format_type is not None:
            return TypeDef(format_type)
        else:
            warnings.warn(f"Unknown format {schema_format!r} for type "
                          f"{schema_type!r}")
    return TypeDef(SWAGGER_PRIMITIVE_TYPES[schema_type])


def get_response_type(spec: Spec, rschema: Dict[str, Any]) -> TypeDef:
    """Extract type information for a given response schema."""
    rschema = spec.deref(rschema)
    if "schema" in rschema:
        return get_type(spec, rschema["schema"])
    return TypeDef("None")
