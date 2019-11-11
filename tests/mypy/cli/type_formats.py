from example import XExampleC

client: XExampleC
reveal_type(client.resource)  # note: Revealed type is 'example.XresourceR'
reveal_type(client.resource.operation)  # note: Revealed type is 'example.XoperationO'
model = client.get_model('Model')()
reveal_type(model)  # note: Revealed type is 'example.XModelM'
