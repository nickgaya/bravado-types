import pytest

import example
from example import petstore


@pytest.fixture(scope='module')
def client():
    return example.create_client()


def test_model_init(client):
    Pet = client.get_model('Pet')
    pet = Pet(name='petName', photoUrls=[])
    assert pet.name == 'petName'

    with pytest.raises(RuntimeError):
        petstore.Pet(name='petName', photoUrls=[])


def test_model_isinstance(client):
    Pet = client.get_model('Pet')
    pet = Pet(name='petName', photoUrls=[])
    assert isinstance(pet, Pet)

    with pytest.raises(RuntimeError):
        isinstance(pet, petstore.Pet)


def test_get_pet_by_id(client):
    pet = example.get_pet_by_id(client, 1)
    assert pet.name is not None
