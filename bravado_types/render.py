from enum import Enum
from typing import Any, Callable, Dict, List

import pkg_resources
from mako.lookup import TemplateLookup

from bravado_types.data_model import SpecInfo, ModelInfo, TypeInfo
from bravado_types.types import ARRAY_TYPE_TEMPLATE
from bravado_types.metadata import Metadata

DEFAULT_CLIENT_TYPE_FORMAT = "{}SwaggerClient"
DEFAULT_RESOURCE_TYPE_FORMAT = "{}Resource"
DEFAULT_OPERATION_TYPE_FORMAT = "{}Operation"
DEFAULT_MODEL_TYPE_FORMAT = "{}Model"


class ResponseTypes(str, Enum):
    success = 'success'
    union = 'union'
    any = 'any'


DEFAULT_RESPONSE_TYPES = ResponseTypes.success


class ArrayTypes(str, Enum):
    list = 'list'
    sequence = 'sequence'
    union = 'union'


DEFAULT_ARRAY_TYPES = ArrayTypes.list


class RenderConfig:
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
        model_inheritance: bool = False,
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
            - union: use a union of typing.List and typing.Tuple
        :param response_types: ResponseTypes enum member indicating how
            operation response types should be annotated. A value of 'success'
            indicates that response types should be a union of defined response
            types for 2xx status codes. A value of 'all' indicates that
            response types should be a union of all documented response types.
            A value of 'any' indicates that all operations should be annotated
            as returning Any. If not specified, the default is 'success'.
        :param model_inheritance: If True, the model type hierarchy will
            reflect model inheritance relationships as expressed by the allOf
            schema property. If False, model types will only inherit from
            bravado_core.model.Model.
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

        self.model_inheritance = model_inheritance

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

    def type(self, type_info: TypeInfo) -> str:
        """Get a type string for a TypeInfo object."""
        type_str = (self.model_type(type_info.base_type) if type_info.is_model
                    else type_info.base_type)
        for outer in type_info.outer:
            if outer == ARRAY_TYPE_TEMPLATE:
                outer = self.array_type_template
            type_str = outer.format(type_str)
        return type_str

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


def render(metadata: Metadata, spec: SpecInfo, config: RenderConfig) -> None:
    """
    Render module and stub files for a given Swagger schema.
    :param spec: SpecInfo representing the schema.
    :param config: Rendering config.
    """
    if config.model_inheritance:
        _topo_sort(spec.models)

    template_dirs = []
    if config.custom_templates_dir:
        template_dirs.append(config.custom_templates_dir)
    template_dirs.append(
        pkg_resources.resource_filename(__name__, "templates/"))
    lookup = TemplateLookup(directories=template_dirs)

    py_template = lookup.get_template("module.py.mako")
    with open(config.py_path, "w") as f:
        f.write(py_template.render(metadata=metadata, spec=spec,
                                   config=config))

    pyi_template = lookup.get_template("module.pyi.mako")
    with open(config.pyi_path, "w") as f:
        f.write(pyi_template.render(metadata=metadata, spec=spec,
                                    config=config))

    if config.postprocessor:
        config.postprocessor(config.py_path, config.pyi_path)


def _topo_sort(model_infos: List[ModelInfo]) -> None:
    """Topologically sort list of models by inheritance."""
    minfos = {mi.name: mi for mi in model_infos}
    levels: Dict[str, int] = {}

    def get_level(name: str) -> int:
        if name in levels:
            return levels[name]
        minfo = minfos[name]
        if minfo.parents:
            level = max(map(get_level, minfo.parents)) + 1
        else:
            level = 0
        levels[name] = level
        return level

    model_infos.sort(key=lambda mi: (get_level(mi.name), mi.name))
