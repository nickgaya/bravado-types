from bravado_types.data_model import TypeDef


def test_TypeDef_wrap_model():
    td = TypeDef("Sequence[{}]", "ModelName")
    wtd = td.wrap("Optional[{}]")
    assert wtd.fmt == "Optional[Sequence[{}]]"
    assert wtd.model == "ModelName"


def test_TypeDef_wrap_nomodel():
    td = TypeDef("int")
    wtd = td.wrap("Sequence[{}]")
    assert wtd.fmt == "Sequence[int]"
    assert wtd.model is None


def test_TypeDef_eq():
    assert TypeDef("int") == TypeDef("int")
    assert TypeDef("int") != TypeDef("float")
    assert TypeDef("Sequence[{}]", "Model") == TypeDef("Sequence[{}]", "Model")
    assert TypeDef("Sequence[{}]", "Model") != TypeDef("Optional[{}]", "Model")
    assert (TypeDef("Sequence[{}]", "Model")
            != TypeDef("Sequence[{}]", "Model2"))
    assert TypeDef("Sequence[{}]", "Model") != TypeDef("int")


def test_TypeDef_hash_eq():
    assert hash(TypeDef("int")) == hash(TypeDef("int"))
    assert hash(TypeDef("Sequence[{}]", "Model")) == hash(
        TypeDef("Sequence[{}]", "Model")
    )


def test_TypeDef_hashable():
    tdset = {
        TypeDef("int"),
        TypeDef("float"),
        TypeDef("Sequence[{}]", "Model"),
        TypeDef("Optional[{}]", "Model"),
        TypeDef("Sequence[{}]", "Model2"),
        TypeDef("int"),
        TypeDef("Sequence[{}]", "Model"),
    }
    assert tdset == {
        TypeDef("int"),
        TypeDef("float"),
        TypeDef("Sequence[{}]", "Model"),
        TypeDef("Optional[{}]", "Model"),
        TypeDef("Sequence[{}]", "Model2"),
    }
