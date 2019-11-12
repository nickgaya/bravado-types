import shlex
from datetime import datetime, timezone
from typing import Iterable, Optional

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
                 schema_origin_url: Optional[str],
                 cli_args: Optional[Iterable[str]]):
        self.timestamp = timestamp
        self.bravado_version = bravado_version
        self.bravado_core_version = bravado_core_version
        self.bravado_types_version = bravado_types_version
        self.schema_version = schema_version
        self.schema_origin_url = schema_origin_url
        self.cli_args = cli_args

    @property
    def quoted_cli_args(self) -> str:
        if self.cli_args is None:
            raise ValueError("cli_args not available")
        return ' '.join(map(shlex.quote, self.cli_args))


def get_metadata(spec: Spec, cli_args: Iterable[str] = None):
    return Metadata(
        timestamp=datetime.now(timezone.utc),
        bravado_version=_get_package_version('bravado'),
        bravado_core_version=_get_package_version('bravado-core'),
        bravado_types_version=_get_package_version('bravado-types'),
        schema_version=spec.spec_dict['info']['version'],
        schema_origin_url=spec.origin_url,
        cli_args=cli_args,
    )


def _get_package_version(name: str) -> str:
    return pkg_resources.get_distribution(name).version
