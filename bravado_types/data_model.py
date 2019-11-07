"""Classes representing typing metadata about a Swagger spec."""

from typing import Any, List, Type

from bravado_core.model import Model
from bravado_core.operation import Operation
from bravado_core.param import Param
from bravado_core.resource import Resource
from bravado_core.spec import Spec


class TypeInfo:
    def __init__(self, base_type: str, *outer: str, is_model: bool = False):
        """
        :param base_type: Base type string
        :param outer: Outer layers wrapping the base type, outermost last
        :param is_model: Whether the base type is a model
        """
        self.base_type = base_type
        self.outer = outer
        self.is_model = is_model

    def wrap(self, outer: str) -> 'TypeInfo':
        return TypeInfo(self.base_type, *self.outer, outer,
                        is_model=self.is_model)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, TypeInfo)
                and self.base_type == other.base_type
                and self.outer == other.outer
                and self.is_model == other.is_model)

    def __repr__(self) -> str:
        va = ', '.join(map(repr, self.outer)) if self.outer else ''
        im = ', is_model=True' if self.is_model else ''
        return f'TypeInfo({self.base_type!r}{va}{im})'


class PropertyInfo:
    """Type information about a Swagger model property."""

    def __init__(self, name: str, type: TypeInfo, required: bool):
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

    def __init__(self, param: Param, name: str, type: TypeInfo,
                 required: bool):
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

    def __init__(self, status: str, type: TypeInfo):
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
