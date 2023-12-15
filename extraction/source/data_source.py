from abc import ABC, abstractmethod


class DataSource(ABC): #pragma: no cover
    def __init__(self, validator=None) -> None:
        self.validator = validator

    @property
    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @property
    @abstractmethod
    def clean_data(self):
        pass
