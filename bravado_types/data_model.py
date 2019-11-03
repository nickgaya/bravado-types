"""Classes representing typing metadata about a Swagger spec."""

from typing import Any, List, Optional, Type

from bravado_core.model import Model
from bravado_core.operation import Operation
from bravado_core.param import Param
from bravado_core.resource import Resource
from bravado_core.spec import Spec


class TypeDef:
    """Type annotation, possibly containing a model name."""

    def __init__(self, fmt: str, model: Optional[str] = None):
        """
        :param fmt: Type format string
        :param model: Optional model name
        """
        self.fmt = fmt
        self.model = model

    def wrap(self, fmt: str) -> "TypeDef":
        """Nest this TypeDef inside another type format string."""
        return TypeDef(fmt.format(self.fmt), self.model)

    def __hash__(self) -> int:
        hsh = 1
        hsh = 31 * hsh + hash(self.fmt)
        hsh = 31 * hsh + hash(self.model)
        return hsh

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, TypeDef)
                and self.fmt == other.fmt
                and self.model == other.model)

    def __repr__(self) -> str:
        return (f'TypeDef({self.fmt!r}, {self.model!r})' if self.model
                else f'TypeDef({self.fmt!r})')


class PropertyInfo:
    """Type information about a Swagger model property."""

    def __init__(self, name: str, type: TypeDef, required: bool):
        self.name = name
        self.type = type
        self.required = required

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, PropertyInfo)
                and self.name == other.name
                and self.type == other.type
                and self.required == other.required)

    def __repr__(self) -> str:
        return (f'PropertyInfo({self.name!r}, {self.type!r}, '
                f'{self.required!r})')


class ModelInfo:
    """Type information about a Swagger model."""

    def __init__(self, mclass: Type[Model], name: str, parents: List[str],
                 props: List[PropertyInfo]):
        self.mclass = mclass
        self.name = name
        self.parents = parents
        self.props = props

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, ModelInfo)
                and self.mclass == other.mclass
                and self.name == other.name
                and self.parents == other.parents
                and self.props == other.props)

    def __repr__(self) -> str:
        return (f'ModelInfo({self.mclass!r}, {self.name!r}, {self.parents!r}, '
                f'{self.props!r})')


class ParameterInfo:
    """Type information about a Swagger operation parameter."""

    def __init__(self, param: Param, name: str, type: TypeDef, required: bool):
        self.param = param
        self.name = name
        self.type = type
        self.required = required

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, ParameterInfo)
                and self.param == other.param
                and self.name == other.name
                and self.type == other.type
                and self.required == other.required)

    def __repr__(self) -> str:
        return (f'ParameterInfo({self.param!r}, {self.name!r}, {self.type!r}, '
                f'{self.required!r})')


class ResponseInfo:
    """Type information about a Swagger operation response."""

    def __init__(self, status: str, type: TypeDef):
        self.status = status
        self.type = type

    @property
    def success(self) -> bool:
        return self.status != "default" and 200 <= int(self.status) < 300

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, ResponseInfo)
                and self.status == other.status
                and self.type == other.type)

    def __repr__(self) -> str:
        return f'ResponseInfo({self.status!r}, {self.type!r})'


class OperationInfo:
    """Type information about a Swagger operation."""

    def __init__(self, operation: Operation, name: str,
                 params: List[ParameterInfo], responses: List[ResponseInfo]):
        self.operation = operation
        self.name = name
        self.params = params
        self.responses = responses

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, OperationInfo)
                and self.operation == other.operation
                and self.name == other.name
                and self.params == other.params
                and self.responses == other.responses)

    def __repr__(self) -> str:
        return (f'OperationInfo({self.operation!r}, {self.name!r}, '
                f'{self.params!r}, {self.responses!r})')


class ResourceInfo:
    """Type information about a Swagger resource."""

    def __init__(self, resource: Resource, name: str,
                 operations: List[OperationInfo]):
        self.resource = resource
        self.name = name
        self.operations = operations

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, ResourceInfo)
                and self.resource == other.resource
                and self.name == other.name
                and self.operations == other.operations)

    def __repr__(self) -> str:
        return (f'ResourceInfo({self.resource!r}, {self.name!r}, '
                f'{self.operations!r})')


class SpecInfo:
    """Type information about a Swagger spec."""

    def __init__(self, spec: Spec, models: List[ModelInfo],
                 resources: List[ResourceInfo],
                 operations: List[OperationInfo]):
        self.spec = spec
        self.models = models
        self.resources = resources
        self.operations = operations

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, SpecInfo)
                and self.spec == other.spec
                and self.models == other.models
                and self.resources == other.resources
                and self.operations == other.operations)

    def __repr__(self) -> str:
        return (f'SpecInfo({self.spec!r}, {self.models!r}, '
                f'{self.resources!r}, {self.operations!r})')
