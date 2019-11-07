from bravado_types.data_model import TypeInfo


def test_TypeInfo_wrap_simple():
    ti = TypeInfo('int')
    wti = ti.wrap('typing.List[{}]')
    assert wti.base_type == 'int'
    assert wti.is_model is False
    assert wti.outer == ('typing.List[{}]',)


def test_TypeInfo_wrap_model():
    ti = TypeInfo('Model', is_model=True)
    wti = ti.wrap('typing.List[{}]')
    assert wti.base_type == 'Model'
    assert wti.is_model is True
    assert wti.outer == ('typing.List[{}]',)


def test_TypeInfo_wrap_multiple():
    ti = TypeInfo('Model', is_model=True)
    wti = ti.wrap('typing.List[{}]').wrap('typing.Optional[{}]')
    assert wti.base_type == 'Model'
    assert wti.is_model is True
    assert wti.outer == ('typing.List[{}]', 'typing.Optional[{}]')
