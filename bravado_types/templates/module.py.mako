<%page args="metadata, spec, config" />\
<%include file="header.mako" args="metadata=metadata" />\
"""${config.name} types."""

import sys

from bravado.client import SwaggerClient

__all__ = [
    ${repr(config.client_type)},
% for resource in spec.resources:
    ${repr(config.resource_type(resource.name))},
% endfor
% for operation in spec.operations:
    ${repr(config.operation_type(operation.name))},
% endfor
% for model in spec.models:
    ${repr(config.model_type(model.name))},
% endfor
]

_TYPE_ERROR = "Generated types cannot be used for runtime type checks"
_RUNTIME_ERROR = "Generated types cannot be instantiated at runtime."


if sys.version_info >= (3, 7, 0):
    class _PlaceholderMeta(type):
        def __instancecheck__(self, instance):
            raise TypeError(_TYPE_ERROR)

        def __subclasscheck__(self, subclass):
            raise TypeError(_TYPE_ERROR)

    class _Placeholder(metaclass=_PlaceholderMeta):
        def __init__(self, *args, **kwargs):
            raise RuntimeError(_RUNTIME_ERROR)

    _PLACEHOLDER = _Placeholder
else:
    def _placeholder(*args, **kwargs):
        raise RuntimeError(_RUNTIME_ERROR)

    _PLACEHOLDER = _placeholder


# Client type

class ${config.client_type}(SwaggerClient):
    pass

# Resource types

% for resource in spec.resources:
${config.resource_type(resource.name)} = _PLACEHOLDER
% endfor

# Operation types

% for operation in spec.operations:
${config.operation_type(operation.name)} = _PLACEHOLDER
% endfor

# Model types

% for model in spec.models:
${config.model_type(model.name)} = _PLACEHOLDER
% endfor
