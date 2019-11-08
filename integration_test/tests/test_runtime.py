import random
import typing

import pytest
from bravado.exception import HTTPError
from bravado.client import SwaggerClient

import example
from example import petstore


@pytest.fixture(scope='module')
def client():
    return example.create_client()


def test_client_class(client):
    assert isinstance(client, petstore.PetStoreSwaggerClient)
    assert issubclass(petstore.PetStoreSwaggerClient, SwaggerClient)
    assert petstore.PetStoreSwaggerClient.__name__ == 'PetStoreSwaggerClient'


def test_model_init(client):
    Pet = client.get_model('Pet')
    pet = Pet(name='petName', photoUrls=[])
    assert pet.name == 'petName'

    with pytest.raises(RuntimeError):
        petstore.PetModel(name='petName', photoUrls=[])


def test_model_isinstance(client):
    Pet = client.get_model('Pet')
    pet = Pet(name='petName', photoUrls=[])
    assert isinstance(pet, Pet)

    with pytest.raises(TypeError):
        isinstance(pet, petstore.PetModel)


def test_placeholder_union():
    typing.Optional[petstore.PetModel]
    typing.Union[petstore.UserModel, petstore.PetModel]


def test_api_calls(client):
    pet_id = random.randrange(2**32)

    try:
        example.create_pet(client, pet_id)
    except HTTPError as e:
        # XXX: petstore.swagger.io server returns an undocumented 200 response
        # for the addPet operation, which causes a bravado HTTPError
        if e.status_code == 200:
            pass

    pet = example.get_pet_by_id(client, pet_id)
    assert pet is not None
    assert isinstance(pet, client.get_model('Pet'))
    assert pet.name is not None
