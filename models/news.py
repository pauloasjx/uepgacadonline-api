import datetime
import locale
from dataclasses import dataclass


@dataclass
class News:
    title: str
    subtitle: str
    author: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime = None

    def __post_init__(self):
        if type(self.created_at) == str:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            self.created_at = datetime.datetime.strptime(self.created_at, '%d/%m/%Y - %Hh%M')
        if type(self.updated_at) == str:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            self.updated_at = datetime.datetime.strptime(self.updated_at, '%d/%m/%Y - %Hh%M')
