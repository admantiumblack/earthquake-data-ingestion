from repository.repository_base_class import RepositoryBaseClass


class GCSRepository(RepositoryBaseClass):

    def __construct_file_path(self, file_name):
        file_path = f'gs://{self.bucket}/{file_name}'
        return file_path

    def save(self, data, file_name:str, file_type:str=None, **kwargs):
        file_path = self.__construct_file_path(file_name)

        if file_type is None:
            file_type = file_path.split('.')[-1]
        try:
            method_name = self._get_method_name(file_type)
        except KeyError:
            raise ValueError("Invalid file type")

        getattr(data, method_name)(file_path, **kwargs)
