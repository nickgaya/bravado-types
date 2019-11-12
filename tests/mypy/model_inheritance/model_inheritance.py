import inheritance, no_inheritance

iparent: inheritance.ParentModel
reveal_type(iparent.preq)  # note: Revealed type is 'builtins.int'
reveal_type(iparent.popt)  # note: Revealed type is 'Union[builtins.int, None]'

ichild: inheritance.ChildModel
reveal_type(ichild.preq)  # note: Revealed type is 'builtins.int'
reveal_type(ichild.popt)  # note: Revealed type is 'Union[builtins.int, None]'
reveal_type(ichild.creq)  # note: Revealed type is 'builtins.str'
reveal_type(ichild.copt)  # note: Revealed type is 'Union[builtins.str, None]'

def ipfunc(parent: inheritance.ParentModel) -> None:
    pass

def icfunc(child: inheritance.ChildModel) -> None:
    pass

ipfunc(ichild)
icfunc(iparent)  # error: Argument 1 to "icfunc" has incompatible type "ParentModel"; expected "ChildModel"

nparent: no_inheritance.ParentModel
reveal_type(nparent.preq)  # note: Revealed type is 'builtins.int'
reveal_type(nparent.popt)  # note: Revealed type is 'Union[builtins.int, None]'

nchild: no_inheritance.ChildModel
reveal_type(nchild.preq)  # note: Revealed type is 'builtins.int'
reveal_type(nchild.popt)  # note: Revealed type is 'Union[builtins.int, None]'
reveal_type(nchild.creq)  # note: Revealed type is 'builtins.str'
reveal_type(nchild.copt)  # note: Revealed type is 'Union[builtins.str, None]'

def npfunc(parent: no_inheritance.ParentModel) -> None:
    pass

def ncfunc(child: no_inheritance.ChildModel) -> None:
    pass

npfunc(nchild)  # error: Argument 1 to "npfunc" has incompatible type "ChildModel"; expected "ParentModel"
ncfunc(nparent)  # error: Argument 1 to "ncfunc" has incompatible type "ParentModel"; expected "ChildModel"
