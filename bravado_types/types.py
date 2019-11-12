"""Functions for mapping Swagger definitions to Python types."""

import warnings
from typing import Any, Dict

from bravado_core.schema import get_type_from_schema
from bravado_core.spec import Spec

from bravado_types.config import Config
from bravado_types.data_model import TypeInfo

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
    ('integer', 'int32'): 'int',
    ('integer', 'int64'): 'int',
    ('number', 'float'): 'float',
    ('number', 'double'): 'float',
    ('string', 'byte'): 'bytes',
    ('string', 'date'): 'datetime.date',
    ('string', 'date-time'): 'datetime.datetime',
    ('string', 'password'): 'str',
}


def get_type_info(spec: Spec, schema: Dict[str, Any], config: Config
                  ) -> TypeInfo:
    """
    Get the type of a schema within a Swagger spec.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    schema = spec.deref(schema)
    schema_type = get_type_from_schema(spec, schema)
    if schema_type == "array":
        type_info = _get_array_type_info(spec, schema, config)
    elif schema_type == "object":
        type_info = _get_object_type_info(spec, schema, config)
    elif schema_type in SWAGGER_PRIMITIVE_TYPES:
        type_info = _get_primitive_type_info(spec, schema, config)
    elif schema_type == "file":
        type_info = TypeInfo("typing.Any")
    elif schema_type is None:
        type_info = TypeInfo("typing.Any")
    else:
        warnings.warn(f"Unknown schema type: {schema_type!r}")
        type_info = TypeInfo("typing.Any")

    if schema.get("x-nullable", False):
        type_info = _wrap(type_info, "typing.Optional[{}]")

    return type_info


def _get_array_type_info(spec: Spec, schema: Dict[str, Any], config: Config
                         ) -> TypeInfo:
    """
    Get the type of an array schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    item_type = get_type_info(spec, schema["items"], config)
    return _wrap(item_type, config.array_type_template)


def _get_object_type_info(spec: Spec, schema: Dict[str, Any], config: Config
                          ) -> TypeInfo:
    """
    Get the type of an object schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    if "x-model" in schema:
        return TypeInfo(config.model_type(schema["x-model"]))

    # Special case: allOf with a single item. This may be used to specify a
    # nullable ref, like this:
    #
    # x-nullable: true
    # allOf:
    #   - $ref: '#/definitions/Model'
    if ('allOf' in schema and len(schema['allOf']) == 1
            and 'properties' not in schema):
        return get_type_info(spec, schema['allOf'][0], config)

    return TypeInfo("typing.Mapping[str, typing.Any]")


def _get_primitive_type_info(spec: Spec, schema: Dict[str, Any], config: Config
                             ) -> TypeInfo:
    """
    Get the type of a primitive schema.
    :param spec: Bravado-core spec object
    :param schema: Schema dict
    :return: A TypeInfo for the schema.
    """
    schema_type = schema["type"]
    if "format" in schema:
        schema_format = schema["format"]
        format_key = schema_type, schema_format
        format_type = SWAGGER_FORMATS.get(format_key)
        if config.custom_formats:
            format_type = config.custom_formats.formats.get(
                format_key, format_type)
        if format_type is not None:
            return TypeInfo(format_type)
        else:
            warnings.warn(f"Unknown format {schema_format!r} for type "
                          f"{schema_type!r}")
    return TypeInfo(SWAGGER_PRIMITIVE_TYPES[schema_type])


def get_response_type_info(spec: Spec, rschema: Dict[str, Any], config: Config
                           ) -> TypeInfo:
    """Extract type information for a given response schema."""
    rschema = spec.deref(rschema)
    if "schema" in rschema:
        return get_type_info(spec, rschema["schema"], config)
    return TypeInfo("None")


def _wrap(type_info: TypeInfo, fmt: str) -> TypeInfo:
    return TypeInfo(fmt.format(type_info))
