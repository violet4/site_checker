from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

_url_base: Optional[str] = None
_url_base_filename = 'url_base.txt'


def get_url_base():
    global _url_base
    if _url_base is None:
        with open(_url_base_filename, 'r') as fr:
            _url_base = fr.read().strip()
    return _url_base


@dataclass(frozen=True)
class Project:
    uuid: str
    title: str
    rate_per_hour: Decimal
    available_tasks: int

    @property
    def url(self):
        return get_url_base()+self.uuid
