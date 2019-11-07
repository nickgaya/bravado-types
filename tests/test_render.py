from bravado_types.data_model import TypeInfo
from bravado_types.render import RenderConfig


def test_render_config_type():
    config = RenderConfig(name='Test', path='/tmp/test.py')
    assert config.type(TypeInfo('str')) == 'str'
    assert config.type(TypeInfo('Pet', is_model=True)) == 'Pet'
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]'))
            == 'typing.Optional[str]')
    assert (config.type(TypeInfo('str', 'typing.Sequence[{}]'))
            == 'typing.Sequence[str]')
    assert (config.type(TypeInfo('str', 'typing.Optional[{}]',
                                 'typing.Sequence[{}]'))
            == 'typing.Sequence[typing.Optional[str]]')
    assert (config.type(TypeInfo('str', 'typing.Sequence[{}]',
                                 'typing.Optional[{}]'))
            == 'typing.Optional[typing.Sequence[str]]')
