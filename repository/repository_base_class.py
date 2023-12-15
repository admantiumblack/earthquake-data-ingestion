from abc import ABC, abstractmethod
import pandas as pd


class RepositoryBaseClass(ABC):  # pragma: no cover
    def __init__(self, bucket):
        self.bucket = bucket

    @abstractmethod
    def save(self, data: pd.DataFrame, file_name, file_type):
        raise NotImplementedError()
