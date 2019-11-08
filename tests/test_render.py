from bravado_types.data_model import TypeInfo
from bravado_types.render import ArrayTypes, RenderConfig


def test_render_config_client_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.client_type == 'TestSwaggerClient'


def test_render_config_resource_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.resource_type('pet') == 'petResource'


def test_render_config_operation_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.operation_type('getPet') == 'getPetOperation'


def test_render_config_model_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.model_type('Pet') == 'PetModel'


def test_render_config_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.type(TypeInfo('str')) == 'str'
    assert config.type(TypeInfo('Pet', is_model=True)) == 'PetModel'
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]'))
            == 'typing.Optional[str]')
    assert (config.type(TypeInfo('Pet', 'typing.Optional[{}]', is_model=True))
            == 'typing.Optional[PetModel]')


def test_render_config_type_array_types_list():
    config = RenderConfig(name='Test', path='/tmp/test.py',
                          array_types=ArrayTypes.list)
    assert (config.type(TypeInfo('str', 'typing.List[{}]'))
            == 'typing.List[str]')
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]',
                                 'typing.List[{}]'))
            == 'typing.List[typing.Optional[str]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.Optional[{}]'))
            == 'typing.Optional[typing.List[str]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.List[{}]'))
            == 'typing.List[typing.List[str]]')


def test_render_config_array_types_sequence():
    config = RenderConfig(name='Test', path='/tmp/test.py',
                          array_types=ArrayTypes.sequence)
    assert (config.type(TypeInfo('str', 'typing.List[{}]'))
            == 'typing.Sequence[str]')
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]',
                                 'typing.List[{}]'))
            == 'typing.Sequence[typing.Optional[str]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.Optional[{}]'))
            == 'typing.Optional[typing.Sequence[str]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.List[{}]'))
            == 'typing.Sequence[typing.Sequence[str]]')


def test_render_config_array_types_union():
    config = RenderConfig(name='Test', path='/tmp/test.py',
                          array_types=ArrayTypes.union)
    assert (config.type(TypeInfo('str', 'typing.List[{}]'))
            == 'typing.Union[typing.List[str], typing.Tuple[str, ...]]')
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]',
                                 'typing.List[{}]'))
            == 'typing.Union[typing.List[typing.Optional[str]], '
            'typing.Tuple[typing.Optional[str], ...]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.Optional[{}]'))
            == 'typing.Optional[typing.Union[typing.List[str], '
            'typing.Tuple[str, ...]]]')
    assert (config.type(TypeInfo('str', 'typing.List[{}]',
                                 'typing.List[{}]'))
            == 'typing.Union[typing.List[typing.Union[typing.List[str], '
            'typing.Tuple[str, ...]]], typing.Tuple[typing.Union['
            'typing.List[str], typing.Tuple[str, ...]], ...]]')
