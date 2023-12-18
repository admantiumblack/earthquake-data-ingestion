import pytest
from pytest_mock import MockerFixture
from repository import GCSRepository

class TestGCSRepository:

    def test_successful_save(self, mocker:MockerFixture):
        bucket_name = 'test_bucket'
        save = mocker.MagicMock()
        data = mocker.MagicMock(spec_set=['to_parquet'])
        file_name = 'test.parquet'
        data.to_parquet = save
        file_type = 'parquet'

        repository = GCSRepository(bucket_name)
        repository.save(data, file_name, file_type)

        save.assert_called_once_with(f'gs://{bucket_name}/{file_name}')
    
    def test_no_file_type(self, mocker:MockerFixture):
        bucket_name = 'test_bucket'
        save = mocker.MagicMock()
        data = mocker.MagicMock(spec_set=['to_parquet'])
        file_name = 'test.parquet'
        data.to_parquet = save

        repository = GCSRepository(bucket_name)
        repository.save(data, file_name)

        save.assert_called_once_with(f'gs://{bucket_name}/{file_name}')
    
    def test_invalid_file_type(self, mocker:MockerFixture):
        bucket_name = 'test_bucket'
        data = mocker.MagicMock()
        file_name = 'test.docs'

        repository = GCSRepository(bucket_name)
        with pytest.raises(ValueError, match='Invalid file type'):
            repository.save(data, file_name)

    def test_invalid_data_object(self, mocker:MockerFixture):
        bucket_name = 'test_bucket'
        data = mocker.MagicMock()
        file_name = 'test.csv'

        repository = GCSRepository(bucket_name)
        with pytest.raises(ValueError, match='data must be pandas dataframe object'):
            repository.save(data, file_name)