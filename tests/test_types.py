import pytest
from bravado_core.spec import Spec

from bravado_types.config import ArrayTypes, Config, CustomFormats
from bravado_types.types import get_type_info, get_response_type_info


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'$ref': '#/definitions/Array'},
        'typing.List[typing.Any]',
        id="array_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {}},
        'typing.List[typing.Any]',
        id="array_of_any",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'integer'}},
        'typing.List[int]',
        id="array_of_int",
    ),
    pytest.param(
        {'type': 'array', 'items': {
            'type': 'array', 'items': {'type': 'string'}
        }},
        'typing.List[typing.List[str]]',
        id="array_of_array_of_string",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'object'}},
        'typing.List[typing.Mapping[str, typing.Any]]',
        id="array_of_object",
    ),
    pytest.param(
        {'type': 'array', 'items': {'$ref': '#/definitions/Object'}},
        'typing.List[ObjectModel]',
        id="array_of_model_ref",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string'}, 'x-nullable': True},
        'typing.Optional[typing.List[str]]',
        id="nullable_array",
    ),
    pytest.param(
        {'type': 'array', 'items': {'type': 'string', 'x-nullable': True}},
        'typing.List[typing.Optional[str]]',
        id="array_of_nullable",
    ),
    pytest.param(
        {'$ref': '#/definitions/Object'},
        'ObjectModel',
        id="object_ref",
    ),
    pytest.param(
        {'type': 'object', 'properties': {'id': {'type': 'string'}}},
        'typing.Mapping[str, typing.Any]',
        id="object_not_model",
    ),
    pytest.param(
        {'type': 'object', 'x-model': 'Something'},
        'SomethingModel',
        id="object_model",
    ),
    pytest.param(
        {'type': 'object', 'x-nullable': True},
        'typing.Optional[typing.Mapping[str, typing.Any]]',
        id="object_nullable",
    ),
    pytest.param(
        {'x-nullable': True, 'allOf': [{'$ref': '#/definitions/Object'}]},
        'typing.Optional[ObjectModel]',
        id="object_nullable_ref",
    ),
    pytest.param(
        {'type': 'integer'},
        'int',
        id="primitive_integer",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int32'},
        'int',
        id="primitive_integer_int32",
    ),
    pytest.param(
        {'type': 'integer', 'format': 'int64'},
        'int',
        id="primitive_integer_int64",
    ),
    pytest.param(
        {'type': 'number'},
        'float',
        id="primitive_number",
    ),
    pytest.param(
        {'type': 'number', 'format': 'float'},
        'float',
        id="primitive_number_float",
    ),
    pytest.param(
        {'type': 'number', 'format': 'double'},
        'float',
        id="primitive_number_double",
    ),
    pytest.param(
        {'type': 'string'},
        'str',
        id="primitive_string",
    ),
    pytest.param(
        {'type': 'string', 'format': 'byte'},
        'bytes',
        id="primitive_string_byte",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date'},
        'datetime.date',
        id="primitive_string_date",
    ),
    pytest.param(
        {'type': 'string', 'format': 'date-time'},
        'datetime.datetime',
        id="primitive_string_date-time",
    ),
    pytest.param(
        {'type': 'string', 'format': 'password'},
        'str',
        id="primitive_string_password",
    ),
    pytest.param(
        {'type': 'boolean'},
        'bool',
        id="primitive_boolean",
    ),
    pytest.param(
        {'type': 'null'},
        'None',
        id="primitive_null",
    ),
    pytest.param(
        {},
        'typing.Any',
        id="no_type",
    ),
])
def test_get_type_info(schema, expected):
    config = Config(name='Test', path='/tmp/test.py')
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
    assert get_type_info(spec, pschema, config) == expected


@pytest.mark.parametrize(('array_types', 'expected'), [
    pytest.param(ArrayTypes.list, 'typing.List[str]',
                 id='list'),
    pytest.param(ArrayTypes.sequence, 'typing.Sequence[str]',
                 id='sequence'),
    pytest.param(ArrayTypes.union,
                 'typing.Union[typing.List[str], typing.Tuple[str, ...]]',
                 id='union'),
])
def test_get_type_info_array_types_list(array_types, expected):
    spec_dict = {
        'swagger': '2.0',
        'info': {
            'title': 'Example schema',
            'version': '1.0',
        },
        'paths': {},
        'definitions': {
            'Object': {
                'type': 'object',
                'properties': {
                    # Schema to be tested
                    'test': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                        },
                    },
                },
            },
        },
    }
    spec = Spec.from_dict(spec_dict)
    pschema = spec.definitions['Object']._model_spec['properties']['test']
    config = Config(name='Test', path='/tmp/test.py', array_types=array_types)
    assert get_type_info(spec, pschema, config) == expected


def test_get_type_info_custom_format():
    spec_dict = {
        'swagger': '2.0',
        'info': {
            'title': 'Example schema',
            'version': '1.0',
        },
        'paths': {},
        'definitions': {
            'ModelWithCustomFormat': {
                'type': 'object',
                'properties': {
                    'test': {
                        'type': 'string',
                        'format': 'ipv4',
                    },
                },
            },
        },
    }
    spec = Spec.from_dict(spec_dict)
    pschema = (spec.definitions['ModelWithCustomFormat']
               ._model_spec['properties']['test'])
    custom_formats = CustomFormats(
        formats={('string', 'ipv4'): 'ipaddress.IPV4Address'},
        packages=('ipaddress'),
    )
    config = Config(name='Test', path='/tmp/test.py',
                    custom_formats=custom_formats)
    assert get_type_info(spec, pschema, config) == 'ipaddress.IPV4Address'


@pytest.mark.parametrize(('schema', 'expected'), [
    pytest.param(
        {'description': '...'},
        'None',
        id="no_schema",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'string'}},
        'str',
        id="schema_primitive",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'object'}},
        'typing.Mapping[str, typing.Any]',
        id="schema_object",
    ),
    pytest.param(
        {'description': '...', 'schema': {'type': 'file'}},
        'typing.Any',
        id="schema_file",
    ),
    pytest.param(
        {'description': '...', 'schema': {
            'type': 'array', 'items': {'$ref': '#/definitions/Object'}
        }},
        'typing.List[ObjectModel]',
        id="schema_array",
    ),
    pytest.param(
        {'description': '...', 'schema': {'$ref': '#/definitions/Object'}},
        'ObjectModel',
        id="schema_ref",
    ),
    pytest.param(
        {'$ref': '#/responses/responseNoSchema'},
        'None',
        id="ref_no_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchema'},
        'str',
        id="ref_with_schema",
    ),
    pytest.param(
        {'$ref': '#/responses/responseWithSchemaRef'},
        'ObjectModel',
        id="ref_with_schema_ref",
    ),
])
def test_get_response_type_info(schema, expected):
    config = Config(name='Test', path='/tmp/test.py')
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
            'Object': {
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
                'schema': {'$ref': '#/definitions/Object'},
            },
        },
    }
    spec = Spec.from_dict(spec_dict)
    operation = spec.resources['rsc'].operations['op']
    rschema = operation.op_spec['responses']['200']
    assert rschema == schema
    assert get_response_type_info(spec, rschema, config) == expected
