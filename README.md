# bravado-types

Tool to generate MyPy type stubs for Bravado-generated classes to support
static type checking.

## Motivation

[Bravado](https://github.com/Yelp/Bravado) is an excellent library for
interacting with APIs defined by Swagger schemas. Unlike some Swagger-based
tools that generate code at build-time that can be integrated with a given
project, Bravado parses the schema at runtime and dynamically generates classes
to represent the data types defined by the schema. This means that static
type-checking tools like MyPy have limited usefulness since attributes
and method signatures are not known until runtime.

Bravado-types attempts to improve this situation by using Bravado at build time
to parse the schema and output type information for static type checking
purposes. Using the generated type stubs, MyPy can detect errors such as
calling a nonexistent operation method on a resource, failing to specify a
required operation parameter, or assigning a wrongly-typed value to a model
attribute. Assuming the schema does not change, this allows for greater
confidence that the code is using the client correctly.

## Usage

### Installation

To install directly from the GitHub master branch:

    pip install -U https://github.com/nickgaya/bravado-types/tarball/master

### Code generation

Using the CLI:

    python3 -m bravado_types \
        --url 'https://petstore.swagger.io/v2/swagger.json' \
        --name PetStore --path petstore.py

This command will download the PetStore example schema and generate a Python 3
module, *petstore.py*, along with a MyPy stub file *petstore.pyi*, for that
schema. The generated module and type stubs can then be added to your package.

Code generation can also be done programmatically.

    from bravado import SwaggerClient
    from bravado_types import RenderConfig, generate_module

    client = SwaggerClient.from_url(
        "https://petstore.swagger.io/v2/swagger.json")
    config = RenderConfig(name='PetStore', path='petstore.py')
    generate_module(client, config)

### Using the generated module

To create a type-aware client, import the relevant name from the generated
module and use its `from_url()` or `from_spec()` method to create an instance.

    from petstore import PetStoreClient

    client = PetStoreClient.from_url(
        "https://petstore.swagger.io/v2/swagger.json")
    reveal_type(client)  # petstore.PetStoreClient

You can use the client like a regular Bravado Swagger client to instantiate
model objects and make API calls with them.

    Pet = client.get_model('Pet')
    reveal_type(Pet)  # Type[petstore.Pet]

    frank = Pet(name='Frank', photoUrls=[])
    reveal_type(frank)  # petstore.Pet

    pet123 = client.pet.getPetById(id=123).response().result
    reveal_type(pet123)  # petstore.Pet

You can also import model types from the generated module for use in type
annotations. Note that imported model types should only be used in annotations,
never called directly.

    from petstore import Pet as TPet

    def get_name(pet: TPet) -> str:
        reveal_type(pet)  # petstore.Pet
        return pet.name

### Configuration

Bravado-types supports several optional parameters to customize code
generation. See the `bravado_types.render.RenderConfig` docstring or the output
of `python -m bravado_types --help` for details.

## Caveats

### Operation response types

Operations often have multiple different response schemas for different status
codes, which presents an obstacle to static type analysis.  Bravado-types
offers three different options for response type annotations, specified by the
`response_types` configuration parameter.

* `'success'`: The response type will be declared as the union of all response
  types with 2xx status. This is unsound, but may be useful if you are primarily
  concerned with responses when the request was successful.

* `'union'`: The response type will be declared as the union of all response
  types defined in the schema. This is probably the most correct but is
  cumbersome, as the developer must perform manual type checks or casts to
  obtain a useable type.

* `'any'`: The response type will be declared as `Any`. This gives maximum
  flexibility but requires the developer to manually add type hints if they
  want any type checking on the result of an operation.

By default, bravado-types uses the `'success'` option as it is felt to be the
most pragmatic option, although the least sound.

### Custom formats

If bravado-types encounters a primitive type spec with an unrecognized 'format'
property, it emits a warning and assigning the variable a type based on the
'type' property alone.

Future versions of this tool may add support for custom user-defined formats.

### Model inheritance

Swagger allows composing model definitions with the `allOf` schema property.
This can be interpreted as a subclass relationship between models. Bravado
implements this to some extent in its model metaclass,
`bravado_core.model.ModelMeta`.

By default, bravado-types does not mirror this implied type hierarchy in its
generated types.  To enable this functionality, set the `model_inheritance`
configuration parameter to `True`.

### Additional properties

Bravado-types does not currently support accessing or setting additional
properties as model class attributes. If you need to set or access additional
properties, you can use dict-like syntax instead.

For example, given this model schema...

    x-model: APModel
    type: object
    additionalProperties:
      type: int

...you can add a property called "something" with the following code:

    model = APModel()
    model['something'] = 123

MyPy will not type-check additional properties.

### File parameters and responses

Bravado's handling of parameters and responses with `type: file` is
complicated.  This tool simply annotates such values with the `Any` type.

## Development

This project uses Tox to run tests and other self-checks.  Unit tests are
written with the Pytest framework.

**Note:** This project is not affiliated with Yelp or the Bravado project.
