from datetime import datetime, timezone
from typing import Optional

import pkg_resources
from bravado_core.spec import Spec


class Metadata:
    """Code generation metadata, used to generate file header comments."""
    def __init__(self,
                 timestamp: datetime,
                 bravado_version: str,
                 bravado_core_version: str,
                 bravado_types_version: str,
                 schema_version: str,
                 schema_origin_url: Optional[str]):
        self.timestamp = timestamp
        self.bravado_version = bravado_version
        self.bravado_core_version = bravado_core_version
        self.bravado_types_version = bravado_types_version
        self.schema_version = schema_version
        self.schema_origin_url = schema_origin_url


def get_metadata(spec: Spec):
    return Metadata(
        timestamp=datetime.now(timezone.utc),
        bravado_version=_get_package_version('bravado'),
        bravado_core_version=_get_package_version('bravado-core'),
        bravado_types_version=_get_package_version('bravado-types'),
        schema_version=spec.spec_dict['info']['version'],
        schema_origin_url=spec.origin_url,
    )


def _get_package_version(name: str) -> str:
    return pkg_resources.get_distribution(name).version
