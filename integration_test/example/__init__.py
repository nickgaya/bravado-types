from example.petstore import PetStoreClient, Pet as TPet


def create_client() -> PetStoreClient:
    return PetStoreClient.from_url(
        'https://petstore.swagger.io/v2/swagger.json')


def create_pet(client: PetStoreClient, id: int) -> None:
    Pet = client.get_model('Pet')
    pet = Pet(id=id, name='New Pet', photoUrls=[])
    response = client.pet.addPet(body=pet).response()
    status_code = response.metadata.status_code
    if not 200 <= status_code < 300:
        raise Exception(f"Create operation unsuccessful: {status_code}")


def get_pet_by_id(client: PetStoreClient, id: int) -> TPet:
    response = client.pet.getPetById(petId=id).response()
    status_code = response.metadata.status_code
    if not 200 <= status_code < 300:
        raise Exception(f"Get operation unsuccessful: {status_code}")
    assert response.result is not None
    return response.result
