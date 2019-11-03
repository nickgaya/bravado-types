<%page args="config, spec" />\
"""${config.name} types."""

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

_RUNTIME_ERROR = ("Generated types should only be used in type annotations, "
                  "not at runtime.")


class _PlaceholderMeta(type):
    def __instancecheck__(self, instance):
        raise RuntimeError(_RUNTIME_ERROR)

    def __subclasscheck__(self, subclass):
        raise RuntimeError(_RUNTIME_ERROR)

    def __getattr__(self, *args, **kwargs):
        raise RuntimeError(_RUNTIME_ERROR)


class _Placeholder(metaclass=_PlaceholderMeta):
    def __init__(self, *args, **kwargs):
        raise RuntimeError(_RUNTIME_ERROR)


# Client type. At runtime, this is just an alias for
# bravado.client.SwaggerClient

${config.client_type} = SwaggerClient

# Resource types

% for resource in spec.resources:
${config.resource_type(resource.name)} = _Placeholder
% endfor

# Operation types

% for operation in spec.operations:
${config.operation_type(operation.name)} = _Placeholder
% endfor

# Model types

% for model in spec.models:
${config.model_type(model.name)} = _Placeholder
% endfor
