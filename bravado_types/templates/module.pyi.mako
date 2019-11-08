<%page args="metadata, spec, config" />\
<%include file="header.mako" args="metadata=metadata" />\
import datetime
import typing
import typing_extensions

import bravado.client
import bravado.http_client
import bravado.http_future
import bravado_core.model
import bravado_core.operation
import bravado_core.resource
import bravado_core.spec

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

class ${config.client_type}(bravado.client.SwaggerClient):
    def __init__(self, swagger_spec: bravado_core.spec.Spec,
                 also_return_response: bool = False) -> None:
% for resource in spec.resources:
        self.${resource.name}: ${repr(config.resource_type(resource.name))}
% endfor
        self.swagger_spec = swagger_spec

    @classmethod
    def from_url(cls, spec_url: str,
                 http_client: bravado.http_client.HttpClient = None,
                 request_headers: typing.Mapping = None,
                 config: typing.Mapping = None
                ) -> ${repr(config.client_type)}: ...

    @classmethod
    def from_spec(cls, spec_dict: typing.Mapping[str, typing.Any],
                  origin_url: str = None,
                  http_client: bravado.http_client.HttpClient = None,
                  config: typing.Mapping = None
                 ) -> ${repr(config.client_type)}: ...

% if spec.models:
    % for model in spec.models:
    @typing.overload
    def get_model(self, model_name: typing_extensions.Literal[${repr(model.name)}]) -> typing.Type[${repr(config.model_type(model.name))}]: ...
    % endfor
    @typing.overload
    def get_model(self, model_name: str) -> typing.Union[
    % for model in spec.models:
        typing.Type[${repr(config.model_type(model.name))}],
    % endfor
    ]: ...

% endif
    @typing.no_type_check
    def __getattr__(self, attr): ...

class _Resource(bravado_core.resource.Resource):
    @typing.no_type_check
    def __getattr__(self, attr): ...

% for resource in spec.resources:
class ${config.resource_type(resource.name)}(_Resource):
    % for operation in resource.operations:
    ${operation.name}: ${repr(config.operation_type(operation.name))}
    % endfor

% endfor
_Operation = bravado_core.operation.Operation

% for operation in spec.operations:
class ${config.operation_type(operation.name)}(_Operation):
    def __call__(
        self,
        *,
        % for param in operation.params:
            % if param.required:
        ${param.name}: ${config.type(param.type)},
            %else:
        ${param.name}: ${config.type(param.type)} = None,
            % endif
        % endfor
        _request_options: typing.Mapping[str, typing.Any] = None,
    ) -> bravado.http_future.HttpFuture[
        % if config.response_types == 'success':
            % if any(response.success for response in operation.responses):
        typing.Union[
                % for response in operation.responses:
                    % if response.success:
                ${config.type(response.type)},  # ${response.status}
                    % endif
                % endfor
        ]
            % else:
        None  # No documented 2xx responses
            % endif
        % elif config.response_types == 'union':
        typing.Union[
            % for response in operation.responses:
            ${config.type(response.type)},  # ${response.status}
            % endfor
            % if operation.default_rtype:
            ${config.type(operation.default_rtype)},  # default
            % endif
        ]
        % else:
        typing.Any
        % endif
    ]: ...

% endfor
class _Model(bravado_core.model.Model):
    @typing.no_type_check
    def __getattr__(self, attr): ...

    @typing.no_type_check
    def __setattr__(self, attr, value): ...

    @typing.no_type_check
    def __delattr__(self, attr, value): ...

% for model in spec.models:
    % if config.model_inheritance:
class ${config.model_type(model.name)}(
        % for parent in model.parents:
    ${parent},
        % endfor
    _Model
):
    % else:
class ${config.model_type(model.name)}(_Model):
    % endif
    def __init__(
        self,
    % if model.props:
        *,
    % endif
    % for prop in model.props:
        % if prop.required:
        ${prop.name}: ${config.type(prop.type)},
        % else:
        ${prop.name}: ${config.type(prop.type)} = None,
        % endif
    % endfor
    ) -> None:
    % if not model.props:
        ...
    % endif
    % for prop in model.props:
        self.${prop.name} = ${prop.name}
    % endfor
    % if not loop.last:

    % endif
% endfor
