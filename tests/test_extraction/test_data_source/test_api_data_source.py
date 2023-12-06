import pytest
from pytest_mock import MockerFixture
from extraction.source import APIDataSource
from extraction.source.api_data_source import get


class TestAPIDataSource:

    @pytest.fixture
    def setup(self, mocker):
        self.mock_validator = mocker.MagicMock()
        self.validator_properties = {
            'validate.return_value': True,
            'document': {
                "testDoc": 'value'
            }
        }
        self.mock_validator.configure_mock(**self.validator_properties)
        self.url = 'https://test.com'
        self.default_params = {
            "test": "test",
            "date": "2022-12-12"
        }

        self.data_source = APIDataSource(self.url, self.default_params, self.mock_validator) 
    
    @pytest.fixture
    def mock_request(self, mocker):
        def response_factory(status_code=200):
            mock_response = mocker.MagicMock()
            response_properties = {
                'status_code': status_code,
                'json.return_value': {
                    'res': "test"
                }
            }
            mock_response.configure_mock(**response_properties)
            self.get = mocker.patch('extraction.source.api_data_source.get', return_value=mock_response)
            return mock_response
        return response_factory

    def test_query_source_success(self, setup, mock_request):
        mock_response = mock_request()

        res = self.data_source.query_source({'test': 'not_test'})
        self.default_params.update({'test':'not_test'})
        self.get.assert_called_once_with(self.url, self.default_params)
        mock_response.json.assert_called_once()
        assert res == self.data_source
    
    def test_failed_query(self, setup, mock_request):
        _ = mock_request(False)
        with pytest.raises(RuntimeError):
            _ = self.data_source.query_source({'test': 'not_test'})
    
    
    def test_data_property_not_set(self, setup):

        with pytest.raises(AttributeError):
            self.data_source.data
    
    def test_validate(self, setup, mock_request):
        mock_request()
        res = self.data_source.query_source().validate()

        assert res == self.data_source
        assert self.data_source.data_valid == True
    
    def test_validate_no_data(self, setup):
        with pytest.raises(AttributeError):
            _ = self.data_source.validate()
    
    def test_clean_data(self, setup):
        self.data_source.data_valid = True
        res = self.data_source.clean_data
        assert res == {"testDoc": 'value'}
    
    def test_invalid_clean_data(self, setup):
        self.data_source.data_valid = False
        with pytest.raises(RuntimeError):
            _ = self.data_source.clean_data
    
    def test_clean_data_no_validation(self, setup):
        with pytest.raises(AttributeError):
            _ = self.data_source.clean_data
