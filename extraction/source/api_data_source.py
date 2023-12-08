from requests import get
from typing import Dict
from datetime import datetime
from extraction.source import DataSource


class APIDataSource(DataSource):
    def __init__(self, url, default_param: Dict = dict(), validator=None, *, parameter_mapping={}) -> None:
        super().__init__(validator)
        self.default_param = default_param
        self.url = url
        self.parameter_mapping = parameter_mapping
    
    def construct_parameter(self, namespaces, parameter={}):
        for parameter_name in self.parameter_mapping:
            if hasattr(namespaces, self.parameter_mapping[parameter_name]):
                parameter[parameter_name] = getattr(namespaces, self.parameter_mapping[parameter_name])
        return parameter

    def query_source(
        self, parameters: Dict[str, str | datetime | int] = dict()
    ) -> DataSource:
        query_parameters = self.default_param.copy()
        query_parameters.update(parameters)
        response = get(self.url, query_parameters)

        if response.status_code != 200:
            raise RuntimeError(f"{self.url} data query failed")

        self.__data = response.json()
        return self

    @property
    def data(self):
        try:
            return self.__data.copy()
        except AttributeError:
            raise AttributeError("data has not been fetched")

    def validate(self) -> DataSource:
        try:
            self.data_valid = self.validator.validate(self.__data)
        except AttributeError:
            raise AttributeError("data has not been fetched")

        return self

    @property
    def clean_data(self):
        try:
            if not self.data_valid:
                raise RuntimeError("data invalid")
        except AttributeError:
            raise AttributeError("data is not validated")

        return self.validator.document
