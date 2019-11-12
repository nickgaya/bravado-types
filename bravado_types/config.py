from enum import Enum
from typing import Any, Callable, Iterable, Mapping, Tuple

DEFAULT_CLIENT_TYPE_FORMAT = "{}SwaggerClient"
DEFAULT_RESOURCE_TYPE_FORMAT = "{}Resource"
DEFAULT_OPERATION_TYPE_FORMAT = "{}Operation"
DEFAULT_MODEL_TYPE_FORMAT = "{}Model"

DEFAULT_MODEL_INHERITANCE = False


class ArrayTypes(str, Enum):
    list = 'list'
    sequence = 'sequence'
    union = 'union'


DEFAULT_ARRAY_TYPES = ArrayTypes.list


class ResponseTypes(str, Enum):
    success = 'success'
    all = 'all'
    any = 'any'


DEFAULT_RESPONSE_TYPES = ResponseTypes.success


class CustomFormats:
    """Type information for custom formats."""
    def __init__(self,
                 formats: Mapping[Tuple[str, str], str],
                 packages: Iterable[str] = ()):
        """
        :param formats: Mapping from (type, format) tuples to type strings
        :param packages: Set of packages to import
        """
        self.formats = formats
        self.packages = sorted(set(packages))
        for package in self.packages:
            parts = package.split('.')
            if not all(part.isidentifier() for part in parts):
                raise ValueError(f"Invalid package name: {package!r}")


class Config:
    def __init__(
        self,
        *,
        name: str,
        path: str,
        client_type_format: str = None,
        resource_type_format: str = None,
        operation_type_format: str = None,
        model_type_format: str = None,
        array_types: ArrayTypes = None,
        response_types: ResponseTypes = None,
        model_inheritance: bool = None,
        custom_formats: CustomFormats = None,
        custom_templates_dir: str = None,
        postprocessor: Callable[[str, str], Any] = None,
    ):
        """
        :param name: Schema name. Should be a valid Python identifier.
        :param path: Path of generated module file. Must end with '.py'.
        :param client_type_format: Format string for generated client type.
        :param resource_type_format: Format string for generated resource
            types.
        :param operation_type_format: Format string for generated operation
            types.
        :param model_type_format: Format string for generated model types.
        :param array_types: ArrayTypes member indicating how to represent array
            types in the schema.
            - list: Use typing.List. This is the default behavior.
            - sequence: Use typing.Sequence
            - union: Use a union of typing.List and typing.Tuple
        :param response_types: ResponseTypes member indicating how to represent
            operation response types.
            - success: Use a union of defined response types for 2xx status
                       codes. This is the default behavior.
            - all: Use a union of all defined response type.
            - any: Use Any for all operation responses.
        :param model_inheritance: If True, the model type hierarchy will
            reflect model inheritance relationships as expressed by the allOf
            schema property. If False, model types will only inherit from
            bravado_core.model.Model.
        :param custom_formats: Custom format type information.
        :param custom_templates_dir: Optional directory containing custom Mako
            templates.
        :param postprocessor: Optional postprocessing function to call after
            rendering templates. This function should accept two string
            arguments (py_path, pyi_path) indicating the output file paths.
        """
        self.name = name

        if not path.endswith(".py"):
            raise ValueError("Path must end with '.py'")
        self.py_path = path
        self.pyi_path = f"{path}i"

        self.client_type_format = \
            client_type_format or DEFAULT_CLIENT_TYPE_FORMAT
        self.resource_type_format = \
            resource_type_format or DEFAULT_RESOURCE_TYPE_FORMAT
        self.operation_type_format = \
            operation_type_format or DEFAULT_OPERATION_TYPE_FORMAT
        self.model_type_format = model_type_format or DEFAULT_MODEL_TYPE_FORMAT

        self.array_types = array_types or DEFAULT_ARRAY_TYPES
        self.response_types = response_types or DEFAULT_RESPONSE_TYPES

        if model_inheritance is None:
            model_inheritance = DEFAULT_MODEL_INHERITANCE
        self.model_inheritance = model_inheritance

        self.custom_formats = custom_formats

        self.custom_templates_dir = custom_templates_dir
        self.postprocessor = postprocessor

    @property
    def client_type(self) -> str:
        """Get the client type name."""
        return self.client_type_format.format(self.name)

    def resource_type(self, resource_name: str) -> str:
        """Get the type name of a given resource."""
        return self.resource_type_format.format(resource_name)

    def operation_type(self, operation_name: str) -> str:
        """Get the type name of a given operation."""
        return self.operation_type_format.format(operation_name)

    def model_type(self, model_name: str) -> str:
        """Get the type name of a given model."""
        return self.model_type_format.format(model_name)

    @property
    def array_type_template(self) -> str:
        """Return type template string for array types"""
        if self.array_types is ArrayTypes.list:
            return 'typing.List[{}]'
        elif self.array_types is ArrayTypes.sequence:
            return 'typing.Sequence[{}]'
        elif self.array_types is ArrayTypes.union:
            return 'typing.Union[typing.List[{0}], typing.Tuple[{0}, ...]]'
        else:
            raise ValueError("Unexpected ArrayTypes value: "
                             f"{self.array_types!r}")
