import pkg_resources
from mako.lookup import TemplateLookup

from bravado_types.config import Config
from bravado_types.data_model import SpecInfo
from bravado_types.metadata import Metadata


def render(metadata: Metadata, spec: SpecInfo, config: Config) -> None:
    """
    Render module and stub files for a given Swagger schema.
    :param metadata: Code generation metadata.
    :param spec: SpecInfo representing the schema.
    :param config: Code generation configuration.
    """
    template_dirs = []
    if config.custom_templates_dir:
        template_dirs.append(config.custom_templates_dir)
    template_dirs.append(
        pkg_resources.resource_filename(__name__, "templates/"))
    lookup = TemplateLookup(directories=template_dirs)

    py_template = lookup.get_template("module.py.mako")
    with open(config.py_path, "w") as f:
        f.write(py_template.render(metadata=metadata, spec=spec,
                                   config=config))

    pyi_template = lookup.get_template("module.pyi.mako")
    with open(config.pyi_path, "w") as f:
        f.write(pyi_template.render(metadata=metadata, spec=spec,
                                    config=config))

    if config.postprocessor:
        config.postprocessor(config.py_path, config.pyi_path)
