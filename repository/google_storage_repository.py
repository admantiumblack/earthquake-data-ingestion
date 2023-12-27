from repository.repository_base_class import RepositoryBaseClass
from google.cloud import storage


class GCSRepository(RepositoryBaseClass):
    def __init__(self, bucket):
        super().__init__(bucket)
        self.client = storage.Client()

    def save(self, data, file_name: str, file_type: str = None, **kwargs):
        if file_type is None:
            file_type = file_name.split(".")[-1]
        method_name = None
        try:
            method_name = self._get_method_name(file_type)
            mime_type = self._get_mime_type(file_type)
        except KeyError:
            raise ValueError("Invalid file type")

        try:
            save_method = getattr(data, method_name)
        except AttributeError:
            raise ValueError("data must be pandas dataframe object")

        self._save(save_method, file_name, mime_type)

    def _save(self, save_method, file_name, mime_type, **kwargs):  # pragma: no cover
        bucket = self.client.get_bucket(self.bucket)
        file_blob = bucket.blob(file_name)
        if file_blob.exists():
            raise ValueError("File exists")
        file_blob.upload_from_string(save_method(**kwargs), mime_type)
