import os.path

from petstore import PetstoreClient

schema_path = os.path.abspath(os.path.dirname(__file__) + "/schema.json")
client = PetstoreClient.from_url(f"file://{schema_path}")
Pet = client.get_model("Pet")

pet = Pet()  # error: Missing named argument "name" for "Pet"
             # error: Missing named argument "photoUrls" for "Pet"
pet2 = Pet(name=123, photoUrls=[])  # error: Argument "name" to "Pet" has incompatible type "int"; expected "str"
pet.firstName  # error: "Pet" has no attribute "firstName"
client.pat.addPet(body=pet)  # error: "PetstoreClient" has no attribute "pat"
client.user.addPet(body=pet)  # error: "userResource" has no attribute "addPet"
client.pet.findByStatus(status=['available'])  # error: "petResource" has no attribute "findByStatus"; maybe "findPetsByStatus"?
client.user.createUser()  # error: Missing named argument "body" for "__call__" of "createUserOperation"
client.user.createUser(body=pet)  # error: Argument "body" to "__call__" of "createUserOperation" has incompatible type "Pet"; expected "User"
