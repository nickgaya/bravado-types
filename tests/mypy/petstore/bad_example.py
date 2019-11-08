import os.path

from petstore import PetstoreSwaggerClient

client: PetstoreSwaggerClient
Pet = client.get_model("Pet")

pet = Pet()  # error: Missing named argument "name" for "PetModel"
             # error: Missing named argument "photoUrls" for "PetModel"
pet2 = Pet(name=123, photoUrls=[])  # error: Argument "name" to "PetModel" has incompatible type "int"; expected "str"
pet.firstName  # error: "PetModel" has no attribute "firstName"
client.pat.addPet(body=pet)  # error: "PetstoreSwaggerClient" has no attribute "pat"
client.user.addPet(body=pet)  # error: "userResource" has no attribute "addPet"
client.pet.findByStatus(status=['available'])  # error: "petResource" has no attribute "findByStatus"; maybe "findPetsByStatus"?
client.user.createUser()  # error: Missing named argument "body" for "__call__" of "createUserOperation"
client.user.createUser(body=pet)  # error: Argument "body" to "__call__" of "createUserOperation" has incompatible type "PetModel"; expected "UserModel"
