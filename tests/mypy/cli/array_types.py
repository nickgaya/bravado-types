import arrays_list, arrays_sequence, arrays_union

model_list: arrays_list.FooModel
reveal_type(model_list.arr)  # note: Revealed type is 'builtins.list[builtins.str]'
for item in model_list.arr:
    reveal_type(item)  # note: Revealed type is 'builtins.str*'
model_list.arr = ['foo']
model_list.arr = ('foo',)  # error: Incompatible types in assignment (expression has type "Tuple[str]", variable has type "List[str]")
model_list.arr = 'foo'  # error: Incompatible types in assignment (expression has type "str", variable has type "List[str]")
model_list.arr = 1  # error: Incompatible types in assignment (expression has type "int", variable has type "List[str]")
model_list.arr = [1]  # error: List item 0 has incompatible type "int"; expected "str"

model_sequence: arrays_sequence.FooModel
reveal_type(model_sequence.arr)  # note: Revealed type is 'typing.Sequence[builtins.str]'
for item in model_sequence.arr:
    reveal_type(item)  # note: Revealed type is 'builtins.str*'
model_sequence.arr = ['foo']
model_sequence.arr = ('foo',)
model_sequence.arr = 'foo'
model_sequence.arr = 1  # error: Incompatible types in assignment (expression has type "int", variable has type "Sequence[str]")
model_sequence.arr = [1]  # error: List item 0 has incompatible type "int"; expected "str"

model_union: arrays_union.FooModel
reveal_type(model_union.arr)  # note: Revealed type is 'Union[builtins.list[builtins.str], builtins.tuple[builtins.str]]'
for item in model_union.arr:
    reveal_type(item)  # note: Revealed type is 'builtins.str*'
model_union.arr = ['foo']
model_union.arr = ('foo',)
model_union.arr = 'foo'  # error: Incompatible types in assignment (expression has type "str", variable has type "Union[List[str], Tuple[str, ...]]")
model_union.arr = 1  # error: Incompatible types in assignment (expression has type "int", variable has type "Union[List[str], Tuple[str, ...]]")
model_union.arr = [1]  # error: List item 0 has incompatible type "int"; expected "str"
