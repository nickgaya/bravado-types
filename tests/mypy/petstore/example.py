import os.path
from typing import Any

from petstore import PetstoreSwaggerClient, PetModel

client = PetstoreSwaggerClient.from_url('...')
reveal_type(client)  # note: Revealed type is 'petstore.PetstoreSwaggerClient'

Pet = client.get_model("Pet")
reveal_type(Pet)  # note: Revealed type is 'Type[petstore.PetModel]'

frank = Pet(name="Frank", photoUrls=[])
reveal_type(frank)  # note: Revealed type is 'petstore.PetModel'

future = client.pet.addPet(body=frank)
reveal_type(future)  # note: Revealed type is 'bravado.http_future.HttpFuture[None]'

reveal_type(client.pet)  # note: Revealed type is 'petstore.petResource'
reveal_type(client.pet.getPetById)  # note: Revealed type is 'petstore.getPetByIdOperation'

pet123 = client.pet.getPetById(petId=123).response().result
reveal_type(pet123)  # note: Revealed type is 'Union[petstore.PetModel*, None]'

client.pet.getPetById(petId=456, _request_options={
    'headers': {'Example-Header': 'header value'}
})

def get_name(pet: PetModel) -> str:
    reveal_type(pet)  # note: Revealed type is 'petstore.PetModel'
    return pet.name


def instance_check(model: Any):
    if isinstance(model, Pet):
        reveal_type(model)  # note: Revealed type is 'petstore.PetModel'
