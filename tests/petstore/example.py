import os.path
from typing import Any

from petstore import PetStoreClient, Pet as TPet

schema_path = os.path.dirname(os.path.abspath(__file__)) + "/schema.json"
client = PetStoreClient.from_url(f"file://{schema_path}")
reveal_type(client)  # note: Revealed type is 'petstore.PetStoreClient'

Pet = client.get_model("Pet")
reveal_type(Pet)  # note: Revealed type is 'Type[petstore.Pet]'

frank = Pet(name="Frank", photoUrls=[])
reveal_type(frank)  # note: Revealed type is 'petstore.Pet'

future = client.pet.addPet(body=frank)
reveal_type(future)  # note: Revealed type is 'bravado.http_future.HttpFuture[None]'

reveal_type(client.pet)  # note: Revealed type is 'petstore.petResource'
reveal_type(client.pet.getPetById)  # note: Revealed type is 'petstore.getPetByIdOperation'

pet123 = client.pet.getPetById(petId=123).response().result
reveal_type(pet123)  # note: Revealed type is 'Union[petstore.Pet*, None]'


def get_name(pet: TPet) -> str:
    reveal_type(pet)  # note: Revealed type is 'petstore.Pet'
    return pet.name


def instance_check(model: Any):
    if isinstance(model, Pet):
        reveal_type(model)  # note: Revealed type is 'petstore.Pet'
