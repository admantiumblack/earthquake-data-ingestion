from abc import ABC, abstractmethod
import pandas as pd


class RepositoryBaseClass(ABC):  # pragma: no cover
    def __init__(self, bucket):
        self.bucket = bucket
    
    def _get_method_name(self, file_type):
        file_method_by_type = {
            'csv': 'to_csv',
            'parquet': 'to_parquet',
        }

        return file_method_by_type[file_type]

    @abstractmethod
    def save(self, data:pd.DataFrame, file_name:str, file_type:str=None, **kwargs):
        raise NotImplementedError()
