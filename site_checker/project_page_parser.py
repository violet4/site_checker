import json
from typing import Optional
import importlib

from bs4 import BeautifulSoup, Tag


class ParserPlugin:
    def parse(self, html_content: str) -> Optional[dict]:
        """ Parse the HTML content for the target data and return the data as a dictionary."""
        raise NotImplementedError("This method needs to be overridden.")


class DefaultParser(ParserPlugin):
    tag_type: str
    attribute_filter: dict
    attribute_key: str
    json_key: str

    def __init__(self, tag_type:str, attribute_filter:dict, attribute_key:str, json_key:str):
        self.tag_type = tag_type
        self.attribute_filter = attribute_filter
        self.attribute_key = attribute_key
        self.json_key = json_key

    def parse(self, html_content: str) -> Optional[dict]:
        soup = BeautifulSoup(html_content, 'html.parser')
        project_tag = soup.find(self.tag_type, self.attribute_filter)
        if project_tag is None:
            return None
        assert isinstance(project_tag, Tag)
        projects_json_string = project_tag.get(self.attribute_key)
        assert isinstance(projects_json_string, str)
        page_data_json = json.loads(projects_json_string)
        projects_data = page_data_json[self.json_key]
        return projects_data


default_parser = DefaultParser('', {}, '', '')


def load_parser(parser_module: str, parser_class: str) -> ParserPlugin:
    module = importlib.import_module(parser_module)
    parser = getattr(module, parser_class)()
    if not isinstance(parser, ParserPlugin):
        raise ValueError(f"The provided parser must be an instance of ParserPlugin.")
    return parser
