from typing import Union

from bravado.client import SwaggerClient
from bravado_core.spec import Spec

from bravado_types.extract import get_spec_info
from bravado_types.render import RenderConfig, render


def generate_module(client_or_spec: Union[SwaggerClient, Spec],
                    render_config: RenderConfig) -> None:
    """
    Convenience function for extracting spec info and rendering files.

    :param client_or_spec: Swagger client or spec.
    :param render_config: Rendering configuration.
    """
    if isinstance(client_or_spec, SwaggerClient):
        spec_info = get_spec_info(client_or_spec.swagger_spec)
    else:
        spec_info = get_spec_info(client_or_spec)

    render(spec_info, render_config)
