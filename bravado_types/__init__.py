from typing import Union

from bravado.client import SwaggerClient
from bravado_core.spec import Spec

from bravado_types.extract import get_spec_info
from bravado_types.metadata import get_metadata
from bravado_types.render import RenderConfig, render


def generate_module(client_or_spec: Union[SwaggerClient, Spec],
                    render_config: RenderConfig) -> None:
    """
    Convenience function for extracting spec info and rendering files.

    :param client_or_spec: Swagger client or spec.
    :param render_config: Rendering configuration.
    """
    if isinstance(client_or_spec, SwaggerClient):
        spec = client_or_spec.swagger_spec
    else:
        spec = client_or_spec
    metadata = get_metadata(spec)
    spec_info = get_spec_info(spec)
    render(metadata, spec_info, render_config)
