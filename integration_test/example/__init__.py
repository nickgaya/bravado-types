from example.petstore import PetStoreClient, Pet as TPet


def create_client() -> PetStoreClient:
    return PetStoreClient.from_url(
        'https://petstore.swagger.io/v2/swagger.json')


def get_pet_by_id(client: PetStoreClient, id: int) -> TPet:
    response = client.pet.getPetById(petId=id).response()
    status_code = response.metadata.status_code
    if status_code == 200:
        assert response.result is not None
        return response.result
    else:
        raise Exception(f"Unexpected status code: {status_code}")
