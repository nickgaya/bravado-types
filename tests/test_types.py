import pytest
from bravado_core.spec import Spec

from bravado_types.data_model import TypeDef
from bravado_types.types import get_type, get_response_type


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'$ref': '#/definitions/Array'},
        TypeDef('typing.Sequence[typing.Any]'),
        id="array_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {}},
        TypeDef('typing.Sequence[typing.Any]'),
        id="array_of_any",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'integer'}},
        TypeDef('typing.Sequence[int]'),
        id="array_of_int",
    ),
    pytest.param(
        {'type': 'array', 'items': {
            'type': 'array', 'items': {'type': 'string'}
        }},
        TypeDef('typing.Sequence[typing.Sequence[str]]'),
        id="array_of_array_of_string",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'object'}},
        TypeDef('typing.Sequence[typing.Dict[str, typing.Any]]'),
        id="array_of_object",
    ),
    pytest.param(
        {'type': 'array', 'items': {'$ref': '#/definitions/Object'}},
        TypeDef('typing.Sequence[{}]', 'Object'),
        id="array_of_model_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string'}, 'x-nullable': True},
        TypeDef('typing.Optional[typing.Sequence[str]]'),
        id="nullable_array",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string', 'x-nullable': True}},
        TypeDef('typing.Sequence[typing.Optional[str]]'),
        id="array_of_nullable",
    ),
    pytest.param(
        {'$ref': '#/definitions/Object'},
        TypeDef('{}', 'Object'),
        id="object_ref",
    ),
    pytest.param(
        {'type': 'object', 'properties': {'id': {'type': 'string'}}},
        TypeDef('typing.Dict[str, typing.Any]'),
        id="object_not_model",
    ),
    pytest.param(
        {'type': 'object', 'x-model': 'Something'},
        TypeDef('{}', 'Something'),
        id="object_model",
    ),
    pytest.param(
        {'type': 'object', 'x-nullable': True},
        TypeDef('typing.Optional[typing.Dict[str, typing.Any]]'),
        id="object_nullable",
    ),
    pytest.param(
        {'x-nullable': True, 'allOf': [{'$ref': '#/definitions/Object'}]},
        TypeDef('typing.Optional[{}]', 'Object'),
        id="object_nullable_ref",
    ),
    pytest.param(
        {'type': 'integer'},
        TypeDef('int'),
        id="primitive_integer",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int32'},
        TypeDef('int'),
        id="primitive_integer_int32",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int64'},
        TypeDef('int'),
        id="primitive_integer_int64",
    ),
    pytest.param(
        {'type': 'number'},
        TypeDef('float'),
        id="primitive_number",
    ),
    pytest.param(
        {'type': 'number', 'format': 'float'},
        TypeDef('float'),
        id="primitive_number_float",
    ),
    pytest.param(
        {'type': 'number', 'format': 'double'},
        TypeDef('float'),
        id="primitive_number_double",
    ),
    pytest.param(
        {'type': 'string'},
        TypeDef('str'),
        id="primitive_string",
    ),
    pytest.param(
        {'type': 'string', 'format': 'byte'},
        TypeDef('bytes'),
        id="primitive_string_byte",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date'},
        TypeDef('datetime.date'),
        id="primitive_string_date",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date-time'},
        TypeDef('datetime.datetime'),
        id="primitive_string_date-time",
    ),
    pytest.param(
        {'type': 'string', 'format': 'password'},
        TypeDef('str'),
        id="primitive_string_password",
    ),
    pytest.param(
        {'type': 'boolean'},
        TypeDef('bool'),
        id="primitive_boolean",
    ),
    pytest.param(
        {'type': 'null'},
        TypeDef('None'),
        id="primitive_null",
    ),
    pytest.param(
        {},
        TypeDef('typing.Any'),
        id="no_type",
    ),
])
def test_get_type(schema, expected):
    spec_dict = {
        'swagger': '2.0',
        'info': {
            'title': 'Example schema',
            'version': '1.0',
        },
        'paths': {},
        'definitions': {
            'Array': {
                'type': 'array',
                'items': {},
            },
            'Object': {
                'type': 'object',
            },
            # Embed test case schema into schema so it get validated by
            # bravado-core. Use property to prevent model discovery from adding
            # an 'x-schema' property to object schemas.
            'Nested': {
                'type': 'object',
                'properties': {
                    'test': schema,
                },
            },
        }
    }
    spec = Spec.from_dict(spec_dict)
    pschema = spec.definitions['Nested']._model_spec['properties']['test']
    assert pschema == schema
    assert get_type(spec, pschema) == expected


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'description': '...'},
        TypeDef('None'),
        id="no_schema",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'string'}},
        TypeDef('str'),
        id="schema_primitive",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'object'}},
        TypeDef('typing.Dict[str, typing.Any]'),
        id="schema_object",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'file'}},
        TypeDef('typing.Any'),
        id="schema_file",
    ),
    pytest.param(
        {'description': '...', 'schema': {
            'type': 'array', 'items': {'$ref': '#/definitions/Model'}
        }},
        TypeDef('typing.Sequence[{}]', 'Model'),
        id="schema_list",
    ),
    pytest.param(
        {'description': '...', 'schema': {'$ref': '#/definitions/Model'}},
        TypeDef('{}', 'Model'),
        id="schema_ref",
    ),
    pytest.param(
        {'$ref': '#/responses/responseNoSchema'},
        TypeDef('None'),
        id="ref_no_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchema'},
        TypeDef('str'),
        id="ref_with_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchemaRef'},
        TypeDef('{}', 'Model'),
        id="ref_with_schema_ref",
    ),
])
def test_get_response_type(schema, expected):
    spec_dict = {
        'swagger': '2.0',
        'info': {
            'title': 'Example schema',
            'version': '1.0',
        },
        'paths': {
            '/test': {
                'get': {
                    'operationId': 'op',
                    'responses': {
                        '200': schema,
                    },
                    'tags': ['rsc'],
                },
            }
        },
        'definitions': {
            'Model': {
                'type': 'object',
            },
        },
        'responses': {
            'responseNoSchema': {
                'description': '...'
            },
            'responseWithSchema': {
                'description': '...',
                'schema': {
                    'type': 'string',
                },
            },
            'responseWithSchemaRef': {
                'description': '...',
                'schema': {'$ref': '#/definitions/Model'},
            },
        },
    }
    spec = Spec.from_dict(spec_dict)
    operation = spec.resources['rsc'].operations['op']
    rschema = operation.op_spec['responses']['200']
    assert rschema == schema
    assert get_response_type(spec, rschema) == expected
