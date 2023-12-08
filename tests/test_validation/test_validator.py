import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from validation.validator import create_validator


class TestValidatorCreator:
    @pytest.fixture
    def setup(self, mocker: MockerFixture):
        self.mocked_validator = self.mocked_data_source = mocker.patch(
            "validation.validator.Validator"
        )

    @pytest.fixture
    def setup_file_read(self, mocker: MockerFixture):
        def mock_file(file_name):
            self.mock_resolver = mocker.patch(
                "validation.validator.resolve_path",
                return_value=Path(f"/ingestion/validation/schema/{file_name}.json"),
            )

            mocked_schema = mocker.mock_open(read_data="test")
            self.mocked_open = mocker.patch("builtins.open", mocked_schema)

            self.mock_file_content = {"name": {"type": "str", "min": 10}}
            self.mock_json_load = mocker.patch(
                "validation.validator.json.load", return_value=self.mock_file_content
            )

        return mock_file

    def test_dictionary_schema(self, setup):
        schema = {"name": {"type": "str", "min": 10}}
        _ = create_validator(schema)

        self.mocked_validator.assert_called_once_with(schema)

    def test_string_schema(self, setup, setup_file_read):
        file_name = "test"
        setup_file_read(file_name)
        _ = create_validator(file_name)

        self.mocked_validator.assert_called_once_with(self.mock_file_content)
        self.mock_resolver.assert_called_once_with(
            f"validation/schema/{file_name}.json"
        )
