import pytest
from pytest_mock import MockerFixture
from pathlib import Path
from utils.path_parser import resolve_path, get_root_directory


def test_resolve_path(mocker:MockerFixture):
    mock_value = Path('/home/test')
    file_name = 'test.py'
    root_dir_mock = mocker.patch('utils.path_parser.get_root_directory')
    root_dir_mock.return_value = mock_value

    path = resolve_path(file_name)
    assert path == (mock_value / file_name)

class TestRootDirectory:


    @pytest.fixture
    def mock_attr(self, mocker:MockerFixture):
        def attr_mocker(getattr_value, hasattr_value=None):
            mocker.patch('sys.frozen', getattr_value, create = True)
            if hasattr_value is not None:
                mocker.patch('sys._MEIPASS', hasattr_value, create = True)
        
        return attr_mocker

    def test_is_frozen(self, mocker:MockerFixture, mock_attr):
        root_dir = 'test'
        mock_attr(True, root_dir)
        res = get_root_directory()
        assert res == Path('test')
    
    @pytest.mark.parametrize(
            'get_value,has_value',
            [
                (True, None),
                (False, 'test')
            ]
    )
    def test_not_frozen(self, mocker:MockerFixture, mock_attr, get_value, has_value):
        root_dir = "test"
        dir_mock = mocker.Mock()
        dir_mock.__file__ = root_dir
        mocker.patch.dict('sys.modules', {
            '__main__': dir_mock
        })
        mock_attr(get_value, has_value)
        res = get_root_directory()
        assert res == Path(root_dir)