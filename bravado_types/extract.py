"""Functions to extract typing metadata from a bravado-core spec."""

from typing import Dict, List, Set, Tuple, Type

from bravado_core.model import Model
from bravado_core.operation import Operation
from bravado_core.param import Param, get_param_type_spec
from bravado_core.resource import Resource
from bravado_core.spec import Spec

from bravado_types.data_model import (ModelInfo, OperationInfo, ParameterInfo,
                                      PropertyInfo, ResourceInfo, ResponseInfo,
                                      SpecInfo)
from bravado_types.types import get_type_info, get_response_type_info


def get_spec_info(spec: Spec) -> SpecInfo:
    """Extract type information for a given spec object."""
    model_infos = _get_model_infos(spec)
    resource_infos, operation_infos = _get_resource_infos(spec)
    return SpecInfo(spec, model_infos, resource_infos, operation_infos)


def _get_model_infos(spec: Spec) -> List[ModelInfo]:
    """Extract model type information for a given spec object."""
    return [
        _get_model_info(spec, name, mclass)
        for name, mclass in sorted(spec.definitions.items())
    ]


def _get_model_info(spec: Spec, name: str, mclass: Type[Model]) -> ModelInfo:
    """Extract type information for a given model class."""
    required_props = _get_required_props(spec, mclass)
    return ModelInfo(
        mclass, name, mclass._inherits_from,
        [
            PropertyInfo(pname, get_type_info(spec, pschema),
                         required=pname in required_props)
            for pname, pschema in sorted(mclass._properties.items())
        ],
    )


def _get_required_props(spec: Spec, mclass: Type[Model]) -> Set[str]:
    mschema = spec.deref(mclass._model_spec)
    required: Set[str] = set()
    seen: Set[str] = set()
    fringe = [mschema]
    while fringe:
        schema = spec.deref(fringe.pop())
        name = schema.get('x-model')
        if name:
            if name in seen:
                continue
            seen.add(name)
        required.update(schema.get("required", []))
        fringe.extend(schema.get('allOf', []))
    return required


def _get_resource_infos(spec: Spec) -> Tuple[List[ResourceInfo],
                                             List[OperationInfo]]:
    """Extract resource/operation type information for a given spec object."""
    ops_cache: Dict[str, OperationInfo] = {}
    return [
        _get_resource_info(spec, name, resource, ops_cache)
        for name, resource in sorted(spec.resources.items())
    ], sorted(ops_cache.values(), key=lambda o: o.name)


def _get_resource_info(spec: Spec, name: str, resource: Resource,
                       ops_cache: Dict[str, OperationInfo]) -> ResourceInfo:
    """Extract type information for a given resource object."""
    return ResourceInfo(
        resource, name,
        [
            _get_operation_info(spec, oname, operation, ops_cache)
            for oname, operation in sorted(resource.operations.items())
        ],
    )


def _get_operation_info(spec: Spec, name: str, operation: Operation,
                        ops_cache: Dict[str, OperationInfo]) -> OperationInfo:
    """Extract type information for a given operation object."""
    if name in ops_cache:
        oinfo = ops_cache[name]
        if operation is not oinfo.operation:
            raise ValueError(f"Non-unique operation id: {name!r}")
    else:
        oinfo = ops_cache[name] = OperationInfo(
            operation, name,
            [
                _get_parameter_info(spec, pname, param)
                for pname, param in sorted(operation.params.items())
            ],
            _get_operation_response_infos(spec, operation),
        )
    return oinfo


def _get_parameter_info(spec: Spec, name: str, param: Param) -> ParameterInfo:
    """Extract type information for a given parameter."""
    ptype = get_type_info(spec, get_param_type_spec(param))
    return ParameterInfo(param, name, ptype, param.required)


def _get_operation_response_infos(spec: Spec, operation: Operation
                                  ) -> List[ResponseInfo]:
    """Extract response type information for a given operation."""
    oschema = spec.deref(operation.op_spec)
    return [
        ResponseInfo(status, get_response_type_info(spec, rschema))
        for status, rschema in sorted(oschema["responses"].items())
    ]
