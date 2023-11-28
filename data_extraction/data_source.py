from requests import get
from typing import Dict
from datetime import datetime
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


class APIDataSource(DataSource):
    def __init__(self, url, validator=None) -> None:
        super().__init__(validator)
        self.url = url

    def query_source(self, parameters: Dict[int | str | datetime]) -> None:
        response = get(self.url, parameters)

        if response.status_code != 200:
            raise RuntimeError(f"{self.url} data query failed")

        self.__data = response.json()
        return self

    @property
    def data(self):
        try:
            return self.__data
        except NameError:
            raise NameError("data has not been fetched")

    def validate(self):
        try:
            self.data_valid = self.validator.validate(self.__data)
        except NameError:
            raise NameError("data has not been fetched")

        return self

    @property
    def clean_data(self):
        try:
            if not self.data_valid:
                raise RuntimeError("data invalid")
        except NameError:
            raise NameError("data is not validated")

        return self.validator.document
