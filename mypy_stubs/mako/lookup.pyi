from typing import List

from mako.template import Template

class TemplateLookup:
    def __init__(self, directories: List[str] = None): ...
    def get_template(self, uri: str) -> Template: ... 
