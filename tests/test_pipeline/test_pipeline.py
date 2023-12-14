import pytest
from pytest_mock import MockerFixture
from pathlib import Path
from process import Pipeline

class TestPipeline:

    @pytest.fixture
    def mock_resolve_path(self, mocker:MockerFixture):
        def resolve_path_mock(filename):
            mocked_resolve_path = mocker.patch('process.pipeline.resolve_path', return_value=Path(filename))
            return mocked_resolve_path
        return resolve_path_mock

    @pytest.fixture
    def mock_parse_steps(self, mocker:MockerFixture):
        def parse_steps_mock(steps):
            mocked_parse_steps = mocker.patch('process.pipeline.parse_steps', return_value=steps)
            return mocked_parse_steps
        return parse_steps_mock
    
    @pytest.fixture
    def mock_open_file(self, mocker:MockerFixture):
        def open_file_mock(functions=None):
            mocked_config = mocker.mock_open(read_data="test")
            mocked_open = mocker.patch("builtins.open", mocked_config)
            mocked_open.side_effect = functions
            
            mocked_safe_open = mocker.patch('process.pipeline.yaml.safe_load', return_value=[{'run':'test', 'name':'test'}])
            return mocked_open, mocked_safe_open
        return open_file_mock
    
    @pytest.fixture
    def process(self, mocker:MockerFixture):
        process_list = [
            mocker.MagicMock(return_value=12, dependancy=[]),
            mocker.MagicMock(return_value=(1, 2), dependancy=[]),
            mocker.MagicMock(return_value=3, dependancy=['test', 'test2'])
        ]
        process_list[0].name = 'test'
        process_list[1].name = 'test2'
        process_list[2].name = 'test3'
        return process_list

    def test_success_list_initialization(self, process):
        pipeline = Pipeline(process)
        assert pipeline.process == process
    
    def test_success_str_initialization(self, mock_resolve_path, mock_parse_steps, mock_open_file):
        mock_resolve_path('config')
        mock_parse_steps([])
        mock_open_file()
        pipeline = Pipeline('config')

        assert pipeline.process == []
    
    def test_invalid_value_initialization(self):

        with pytest.raises(ValueError):
            _ = Pipeline(12)
    
    def test_invalid_config(self, mock_resolve_path, mock_parse_steps, mock_open_file):
        mock_resolve_path('config')
        mock_parse_steps([])
        mock_open_file(OSError)

        with pytest.raises(FileNotFoundError):
            Pipeline('config')

    def test_set_process(self, process):
        pipeline = Pipeline(process)
        pipeline.process = []
        assert pipeline.process == []
    
    def test_set_invalid_process(self, process):
        pipeline = Pipeline(process)
        with pytest.raises(ValueError):
            pipeline.process = 12

    def test_successful_run(self, process):
        pipeline = Pipeline(process)
        data = [12]
        res = pipeline.run(data)

        assert res == process[-1].return_value
        process[0].assert_called_once_with(data)
        process[1].assert_called_once_with(12)
        process[2].assert_called_once_with(12, 1, 2)
    
    def test_invalid_process_dependancy_run(self, process):
        process[-1].dependancy = ['invalid_dependancy']
        pipeline = Pipeline(process)
        data = [12]
        
        with pytest.raises(RuntimeError):
            pipeline.run(data)