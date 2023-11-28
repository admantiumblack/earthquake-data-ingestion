from abc import ABC, abstractmethod


class DataSource(ABC):
    def __init__(self, validator=None) -> None:
        self.validator = validator

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def clean_data(self):
        pass
