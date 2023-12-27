import pytest
from pytest_mock import MockerFixture
from repository import GCSRepository


class TestGCSRepository:

    @pytest.fixture
    def mock_storage_client(self, mocker: MockerFixture):
        return mocker.patch("repository.google_storage_repository.storage.Client")
    
    def test_successful_save(self, mocker: MockerFixture, mock_storage_client):
        bucket_name = "test_bucket"
        to_parquet = mocker.MagicMock()
        data = mocker.MagicMock(spec_set=["to_parquet"])
        file_name = "test.parquet"
        data.to_parquet = to_parquet
        file_type = "parquet"
        

        repository = GCSRepository(bucket_name)
        repository._save = mocker.MagicMock()
        repository.save(data, file_name, file_type)

        repository._save.assert_called_once_with(to_parquet, file_name, 'application/x-parquet')

    def test_no_file_type(self, mocker: MockerFixture, mock_storage_client):
        bucket_name = "test_bucket"
        to_parquet = mocker.MagicMock()
        data = mocker.MagicMock(spec_set=["to_parquet"])
        file_name = "test.parquet"
        data.to_parquet = to_parquet

        repository = GCSRepository(bucket_name)
        repository._save = mocker.MagicMock()
        repository.save(data, file_name)

        repository._save.assert_called_once_with(to_parquet, file_name, 'application/x-parquet')

    def test_invalid_file_type(self, mocker: MockerFixture, mock_storage_client):
        bucket_name = "test_bucket"
        data = mocker.MagicMock()
        file_name = "test.docs"
        repository = GCSRepository(bucket_name)
        with pytest.raises(ValueError, match="Invalid file type"):
            repository.save(data, file_name)

    def test_invalid_data_object(self, mocker: MockerFixture, mock_storage_client):
        bucket_name = "test_bucket"
        data = mocker.MagicMock(spec_set=[])
        file_name = "test.csv"
        repository = GCSRepository(bucket_name)
        with pytest.raises(ValueError, match="data must be pandas dataframe object"):
            repository.save(data, file_name)
