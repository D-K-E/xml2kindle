# dictionary extractor for making kindle dictionaries
# Author: Kaan Eraslan
# License: see, LICENSE

from abc import ABC, abstractmethod
from typing import Set, List, Dict, Any


class EntryExtractor(ABC):
    "Extract from tei xml dictionary based on entry template"

    def __init__(self, entry):
        self.entry = entry

    @abstractmethod
    def get_entry_definitions(self) -> List[str]:
        pass

    @abstractmethod
    def get_entry_id(self) -> str:
        pass

    @abstractmethod
    def get_entry_value(self) -> str:
        pass

    @abstractmethod
    def get_entry_display_value(self) -> str:
        pass

    @abstractmethod
    def get_entry_parameter(self, index_name: str) -> dict:
        pass

class DictExtractor(ABC):
    def __init__(self, index_name):
        pass

    @abstractmethod
    def get_entry_parameters(self):
        pass

    @abstractmethod
    def get_creator(self):
        pass

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_inlang(self):
        pass

    @abstractmethod
    def get_outlang(self):
        pass

    @abstractmethod
    def get_doc_lang(self):
        pass
