"""Functions for mapping Swagger definitions to Python types."""

import warnings
from typing import Any, Dict

from bravado_core.schema import get_type_from_schema
from bravado_core.spec import Spec

from bravado_types.data_model import TypeInfo

# Type template for array types
ARRAY_TYPE_TEMPLATE = 'typing.List[{}]'

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


def get_type_info(spec: Spec, schema: Dict[str, Any]) -> TypeInfo:
    """
    Get the type of a schema within a Swagger spec.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    schema = spec.deref(schema)
    schema_type = get_type_from_schema(spec, schema)
    if schema_type == "array":
        type_info = _get_array_type_info(spec, schema)
    elif schema_type == "object":
        type_info = _get_object_type_info(spec, schema)
    elif schema_type in SWAGGER_PRIMITIVE_TYPES:
        type_info = _get_primitive_type_info(spec, schema)
    elif schema_type == "file":
        type_info = TypeInfo("typing.Any")
    elif schema_type is None:
        type_info = TypeInfo("typing.Any")
    else:
        warnings.warn(f"Unknown schema type: {schema_type!r}")
        type_info = TypeInfo("typing.Any")

    if schema.get("x-nullable", False):
        type_info = type_info.wrap("typing.Optional[{}]")

    return type_info


def _get_array_type_info(spec: Spec, schema: Dict[str, Any]) -> TypeInfo:
    """
    Get the type of an array schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    item_type = get_type_info(spec, schema["items"])
    return item_type.wrap(ARRAY_TYPE_TEMPLATE)


def _get_object_type_info(spec: Spec, schema: Dict[str, Any]) -> TypeInfo:
    """
    Get the type of an object schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    if "x-model" in schema:
        return TypeInfo(schema["x-model"], is_model=True)

    # Special case: allOf with a single item. This may be used to specify a
    # nullable ref, like this:
    #
    # x-nullable: true
    # allOf:
    #   - $ref: '#/definitions/Model'
    if ('allOf' in schema and len(schema['allOf']) == 1
            and 'properties' not in schema):
        return get_type_info(spec, schema['allOf'][0])

    return TypeInfo("typing.Mapping[str, typing.Any]")


def _get_primitive_type_info(spec: Spec, schema: Dict[str, Any]) -> TypeInfo:
    """
    Get the type of a primitive schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    schema_type = schema["type"]
    if "format" in schema:
        schema_format = schema["format"]
        format_type = SWAGGER_FORMATS.get(schema_type, {}).get(schema_format)
        if format_type is not None:
            return TypeInfo(format_type)
        else:
            warnings.warn(f"Unknown format {schema_format!r} for type "
                          f"{schema_type!r}")
    return TypeInfo(SWAGGER_PRIMITIVE_TYPES[schema_type])


def get_response_type_info(spec: Spec, rschema: Dict[str, Any]) -> TypeInfo:
    """Extract type information for a given response schema."""
    rschema = spec.deref(rschema)
    if "schema" in rschema:
        return get_type_info(spec, rschema["schema"])
    return TypeInfo("None")
