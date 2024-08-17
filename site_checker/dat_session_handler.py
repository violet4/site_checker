import os
from typing import Optional
import requests
import csv
import datetime

_default_cookies_path = 'cookies.csv'
_sample_html_path = os.path.join('tests', 'sample_html.html')


def parse_expiration(s:str) -> float:
    if s.lower() == 'session':
        return 0.0
    return datetime.datetime.strptime(s, '%a, %d %b %Y %H:%M:%S %Z').timestamp()


class DATSession(requests.Session):
    _project_url: Optional[str] = None
    _project_url_file = 'project_url.txt'

    def __init__(self, cookies_path:str=_default_cookies_path):
        super().__init__()
        self.cookies_path = cookies_path
        self.load_cookies()

    def load_cookies(self):
        with open(self.cookies_path, 'r') as file:
            csvr = csv.DictReader(file, delimiter='\t')
            for row in csvr:
                expires = parse_expiration(row['expires'])
                self.cookies.set(row['name'], row['value'], domain=row['domain'],
                                 path=row['path'], expires=expires)

    def get_project_webpage(self, debug:bool=False):
        if debug:
            with open(_sample_html_path, 'r') as fr:
                return fr.read()
        response = self.get(self.project_url)
        return response.text

    @property
    def project_url(self):
        if self._project_url is None:
            with open(self._project_url_file, 'r') as fr:
                self._project_url = fr.read().strip()
        return self._project_url
