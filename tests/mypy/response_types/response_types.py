import responses_success, responses_all, responses_any

client_success: responses_success.ExampleSwaggerClient
reveal_type(client_success.resource.example())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_success.FooModel]'
reveal_type(client_success.resource.exampleWithDefault())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_success.FooModel]'
reveal_type(client_success.resource.exampleSuccessOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_success.FooModel]'
reveal_type(client_success.resource.exampleDefaultOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[None]'
reveal_type(client_success.resource.exampleErrorOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[None]'
reveal_type(client_success.resource.exampleMultipleSuccess())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_success.FooModel, responses_success.BarModel]]'
reveal_type(client_success.resource.exampleNoContent())  # note: Revealed type is 'bravado.http_future.HttpFuture[None]'
reveal_type(client_success.resource.exampleMultiple())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_success.FooModel, responses_success.BarModel, None]]'

client_all: responses_all.ExampleSwaggerClient
reveal_type(client_all.resource.example())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_all.FooModel, responses_all.ErrorModel]]'
reveal_type(client_all.resource.exampleWithDefault())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_all.FooModel, responses_all.ErrorModel]]'
reveal_type(client_all.resource.exampleSuccessOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_all.FooModel]'
reveal_type(client_all.resource.exampleDefaultOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_all.ErrorModel]'
reveal_type(client_all.resource.exampleErrorOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[responses_all.ErrorModel]'
reveal_type(client_all.resource.exampleMultipleSuccess())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_all.FooModel, responses_all.BarModel]]'
reveal_type(client_all.resource.exampleNoContent())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[None, responses_all.ErrorModel]]'
reveal_type(client_all.resource.exampleMultiple())  # note: Revealed type is 'bravado.http_future.HttpFuture[Union[responses_all.FooModel, responses_all.BarModel, None, responses_all.ErrorModel, responses_all.ErrorModel, responses_all.ErrorModel]]'

client_any: responses_any.ExampleSwaggerClient
reveal_type(client_any.resource.example())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleWithDefault())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleSuccessOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleDefaultOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleErrorOnly())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleMultipleSuccess())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleNoContent())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
reveal_type(client_any.resource.exampleMultiple())  # note: Revealed type is 'bravado.http_future.HttpFuture[Any]'
