import pytest
from bravado_core.spec import Spec

from bravado_types.data_model import TypeInfo
from bravado_types.types import get_type_info, get_response_type_info


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'$ref': '#/definitions/Array'},
        TypeInfo('typing.Any', 'typing.List[{}]'),
        id="array_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {}},
        TypeInfo('typing.Any', 'typing.List[{}]'),
        id="array_of_any",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'integer'}},
        TypeInfo('int', 'typing.List[{}]'),
        id="array_of_int",
    ),
    pytest.param(
        {'type': 'array', 'items': {
            'type': 'array', 'items': {'type': 'string'}
        }},
        TypeInfo('str', 'typing.List[{}]', 'typing.List[{}]'),
        id="array_of_array_of_string",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'object'}},
        TypeInfo('typing.Mapping[str, typing.Any]', 'typing.List[{}]'),
        id="array_of_object",
    ),
    pytest.param(
        {'type': 'array', 'items': {'$ref': '#/definitions/Object'}},
        TypeInfo('Object', 'typing.List[{}]', is_model=True),
        id="array_of_model_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string'}, 'x-nullable': True},
        TypeInfo('str', 'typing.List[{}]', 'typing.Optional[{}]'),
        id="nullable_array",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string', 'x-nullable': True}},
        TypeInfo('str', 'typing.Optional[{}]', 'typing.List[{}]'),
        id="array_of_nullable",
    ),
    pytest.param(
        {'$ref': '#/definitions/Object'},
        TypeInfo('Object', is_model=True),
        id="object_ref",
    ),
    pytest.param(
        {'type': 'object', 'properties': {'id': {'type': 'string'}}},
        TypeInfo('typing.Mapping[str, typing.Any]'),
        id="object_not_model",
    ),
    pytest.param(
        {'type': 'object', 'x-model': 'Something'},
        TypeInfo('Something', is_model=True),
        id="object_model",
    ),
    pytest.param(
        {'type': 'object', 'x-nullable': True},
        TypeInfo('typing.Mapping[str, typing.Any]', 'typing.Optional[{}]'),
        id="object_nullable",
    ),
    pytest.param(
        {'x-nullable': True, 'allOf': [{'$ref': '#/definitions/Object'}]},
        TypeInfo('Object', 'typing.Optional[{}]', is_model=True),
        id="object_nullable_ref",
    ),
    pytest.param(
        {'type': 'integer'},
        TypeInfo('int'),
        id="primitive_integer",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int32'},
        TypeInfo('int'),
        id="primitive_integer_int32",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int64'},
        TypeInfo('int'),
        id="primitive_integer_int64",
    ),
    pytest.param(
        {'type': 'number'},
        TypeInfo('float'),
        id="primitive_number",
    ),
    pytest.param(
        {'type': 'number', 'format': 'float'},
        TypeInfo('float'),
        id="primitive_number_float",
    ),
    pytest.param(
        {'type': 'number', 'format': 'double'},
        TypeInfo('float'),
        id="primitive_number_double",
    ),
    pytest.param(
        {'type': 'string'},
        TypeInfo('str'),
        id="primitive_string",
    ),
    pytest.param(
        {'type': 'string', 'format': 'byte'},
        TypeInfo('bytes'),
        id="primitive_string_byte",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date'},
        TypeInfo('datetime.date'),
        id="primitive_string_date",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date-time'},
        TypeInfo('datetime.datetime'),
        id="primitive_string_date-time",
    ),
    pytest.param(
        {'type': 'string', 'format': 'password'},
        TypeInfo('str'),
        id="primitive_string_password",
    ),
    pytest.param(
        {'type': 'boolean'},
        TypeInfo('bool'),
        id="primitive_boolean",
    ),
    pytest.param(
        {'type': 'null'},
        TypeInfo('None'),
        id="primitive_null",
    ),
    pytest.param(
        {},
        TypeInfo('typing.Any'),
        id="no_type",
    ),
])
def test_get_type_info(schema, expected):
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
    assert get_type_info(spec, pschema) == expected


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'description': '...'},
        TypeInfo('None'),
        id="no_schema",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'string'}},
        TypeInfo('str'),
        id="schema_primitive",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'object'}},
        TypeInfo('typing.Mapping[str, typing.Any]'),
        id="schema_object",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'file'}},
        TypeInfo('typing.Any'),
        id="schema_file",
    ),
    pytest.param(
        {'description': '...', 'schema': {
            'type': 'array', 'items': {'$ref': '#/definitions/Model'}
        }},
        TypeInfo('Model', 'typing.List[{}]', is_model=True),
        id="schema_list",
    ),
    pytest.param(
        {'description': '...', 'schema': {'$ref': '#/definitions/Model'}},
        TypeInfo('Model', is_model=True),
        id="schema_ref",
    ),
    pytest.param(
        {'$ref': '#/responses/responseNoSchema'},
        TypeInfo('None'),
        id="ref_no_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchema'},
        TypeInfo('str'),
        id="ref_with_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchemaRef'},
        TypeInfo('Model', is_model=True),
        id="ref_with_schema_ref",
    ),
])
def test_get_response_type_info(schema, expected):
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
    assert get_response_type_info(spec, rschema) == expected
