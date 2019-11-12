from custom_formats import ExampleModel

model: ExampleModel
reveal_type(model.noFormat)  # note: Revealed type is 'builtins.str'
reveal_type(model.defaultFormat)  # note: Revealed type is 'datetime.datetime'
reveal_type(model.customFormat)  # note: Revealed type is 'ipaddress.IPv4Address'
reveal_type(model.unknownFormat)  # note: Revealed type is 'builtins.str'
