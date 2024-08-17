from site_checker.project_page_parser import DefaultParser

tag_type = 'div'
attribute_filter = {'id': 'important-stuff'}
attribute_key = 'data_attribute'
json_key = 'info_key'


class SiteParser(DefaultParser):
    def __init__(self, tag_type=tag_type, attribute_filter=attribute_filter, attribute_key=attribute_key, json_key=json_key):
        super().__init__(tag_type, attribute_filter, attribute_key, json_key)
