from bravado_core.spec import Spec

from bravado_types.data_model import (ModelInfo, OperationInfo, ParameterInfo,
                                      PropertyInfo, ResourceInfo, ResponseInfo,
                                      SpecInfo, TypeDef)
from bravado_types.extract import get_spec_info


def test_extract_minimal():
    spec = Spec.from_dict({
        'swagger': '2.0',
        'info': {
            'title': 'Minimal schema',
            'version': '1.0',
        },
        'paths': {},
    })
    spec_info = get_spec_info(spec)
    assert isinstance(spec_info, SpecInfo)
    assert spec_info.spec is spec
    assert spec_info.models == []
    assert spec_info.resources == []
    assert spec_info.operations == []


def test_extract_basic():
    spec = Spec.from_dict({
        'swagger': '2.0',
        'info': {
            'title': 'Simple schema',
            'version': '1.0',
        },
        'paths': {
            '/foo': {
                'post': {
                    'operationId': 'createFoo',
                    'tags': ['foo'],
                    'parameters': [
                        {
                            'name': 'request',
                            'in': 'body',
                            'required': True,
                            'schema': {
                                '$ref': '#/definitions/Foo',
                            },
                        },
                    ],
                    'responses': {
                        '204': {'$ref': '#/responses/successNoContent'},
                    }
                }
            },
            '/foo/{id}': {
                'get': {
                    'operationId': 'getFoo',
                    'tags': ['foo'],
                    'parameters': [
                        {
                            'name': 'id',
                            'in': 'path',
                            'type': 'integer',
                            'required': True,
                        },
                        {'$ref': '#/parameters/headerParam'},
                    ],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'schema': {'$ref': '#/definitions/Foo'},
                        },
                        '404': {
                            'description': 'Not Found',
                            'schema': {},
                        },
                    },
                },
            },
            '/bar': {
                'get': {
                    'operationId': 'getBar',
                    'tags': ['bar'],
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'schema': {'$ref': '#/definitions/Bar'},
                        },
                    },
                },
            },
        },
        'definitions': {
            'Foo': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'foobar': {'type': 'string'},
                },
                'required': ['id'],
            },
            'Bar': {
                'type': 'object',
            },
        },
        'parameters': {
            'headerParam': {
                'name': 'Header-Param',
                'in': 'header',
                'type': 'string',
            },
        },
        'responses': {
            'successNoContent': {
                'description': 'Operation successful, no response content',
            },
        },
    })
    spec_info = get_spec_info(spec)

    assert spec_info.spec is spec

    assert spec_info.models == [
        ModelInfo(spec.definitions['Bar'], 'Bar', [], []),
        ModelInfo(spec.definitions['Foo'], 'Foo', [], [
            PropertyInfo('foobar', TypeDef('str'), False),
            PropertyInfo('id', TypeDef('int'), True),
        ]),
    ]

    createFoo = spec.resources['foo'].operations['createFoo']
    getFoo = spec.resources['foo'].operations['getFoo']
    getBar = spec.resources['bar'].operations['getBar']

    assert spec_info.operations == [
        OperationInfo(createFoo, 'createFoo', [
            ParameterInfo(
                createFoo.params['request'],
                'request', TypeDef('{}', 'Foo'), True),
        ], [
            ResponseInfo('204', TypeDef('None')),
        ]),
        OperationInfo(getBar, 'getBar', [], [
            ResponseInfo('200', TypeDef('{}', 'Bar')),
        ]),
        OperationInfo(getFoo, 'getFoo', [
            ParameterInfo(getFoo.params['Header_Param'], 'Header_Param',
                          TypeDef('str'), False),
            ParameterInfo(getFoo.params['id'], 'id', TypeDef('int'), True),
        ], [
            ResponseInfo('200', TypeDef('{}', 'Foo')),
            ResponseInfo('404', TypeDef('typing.Any')),
        ]),
    ]

    assert spec_info.resources == [
        ResourceInfo(
            spec.resources['bar'], 'bar',
            operations=[spec_info.operations[1]]),
        ResourceInfo(
            spec.resources['foo'], 'foo',
            operations=[spec_info.operations[0], spec_info.operations[2]]),
    ]
