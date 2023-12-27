import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from extraction.extract import get_data_source


class TestHelper:
    @pytest.fixture(autouse=True)
    def mock_read(self, mocker: MockerFixture):
        self.mocked_resolve_path = mocker.patch(
            "extraction.extract.resolve_path",
            return_value=Path("/ingestion/extraction/api_sources/test.yaml"),
        )
        self.mocked_safe_load = mocker.patch(
            "extraction.extract.yaml.safe_load",
            return_value={
                "url": "test",
                "defaults": {"test": "test"},
                "parameter_mapping": {"test": "test"},
            },
        )
        self.mocked_data_source = mocker.patch("extraction.extract.APIDataSource")
        mocked_extraction = mocker.mock_open(read_data="test")
        self.mocked_open = mocker.patch("builtins.open", mocked_extraction)

    def test_get_data_source_by_source_name(self):
        file_name = "test"
        _ = get_data_source(file_name)

        self.mocked_resolve_path.assert_called_once_with(
            "extraction/api_sources/test.yaml"
        )
        self.mocked_open.assert_called_once_with(
            Path("/ingestion/extraction/api_sources/test.yaml"), "r"
        )
        self.mocked_data_source.assert_called_once()

    def test_get_data_source_by_schema(self):
        data_source_details = {
            "url": "test_mock.com",
            "defaults": {"test": "test"},
        }
        _ = get_data_source(data_source_details)

        self.mocked_data_source.assert_called_once_with(
            "test_mock.com", default_param={"test": "test"}, parameter_mapping={}
        )
