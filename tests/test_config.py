import pytest

from bravado_types.config import ArrayTypes, Config


def test_config_client_type():
    config = Config(name='Test', path='/tmp/test.py')
    assert config.client_type == 'TestSwaggerClient'


def test_config_resource_type():
    config = Config(name='Test', path='/tmp/test.py')
    assert config.resource_type('pet') == 'petResource'


def test_config_operation_type():
    config = Config(name='Test', path='/tmp/test.py')
    assert config.operation_type('getPet') == 'getPetOperation'


def test_config_model_type():
    config = Config(name='Test', path='/tmp/test.py')
    assert config.model_type('Pet') == 'PetModel'


@pytest.mark.parametrize(('array_types', 'expected'), [
    pytest.param(ArrayTypes.list, 'typing.List[T]', id='list'),
    pytest.param(ArrayTypes.sequence, 'typing.Sequence[T]', id='sequence'),
    pytest.param(ArrayTypes.union,
                 'typing.Union[typing.List[T], typing.Tuple[T, ...]]',
                 id='union'),
])
def test_config_type_array_types(array_types, expected):
    config = Config(name='Test', path='/tmp/test.py', array_types=array_types)
    assert expected == config.array_type_template.format('T')
