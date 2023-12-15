import pytest
from pytest_mock import MockerFixture
from process.parser import parse_steps


@pytest.fixture
def mock_steps(mocker: MockerFixture):
    def step_mocker(step_list):
        mock_step = mocker.MagicMock(list(step_list.keys()))
        for i in step_list:
            mock_process = mocker.MagicMock()
            mock_process.return_value = step_list[i]
            setattr(mock_step, i, mock_process)

        mock_step = mocker.patch("process.parser.steps", mock_step)
        return mock_step

    return step_mocker


def test_valid_parsing(mock_steps):
    step_definitions = [
        {"run": "test", "name": "test"},
        {"run": "test1", "name": "test1", "dependancy": ["test"]},
        {"run": "test2", "name": "test2", "parameters": ["test", "test", "test"]},
    ]
    steps_to_mock = {"test": "test", "test1": "test1", "test2": "test2"}

    steps = mock_steps(steps_to_mock)

    _ = parse_steps(step_definitions)

    steps.test.assert_called_once_with(name="test", dependancy=[])
    steps.test1.assert_called_once_with(name="test1", dependancy=["test"])
    steps.test2.assert_called_once_with(
        "test", "test", "test", name="test2", dependancy=[]
    )


def test_invalid_process(mock_steps):
    step_definitions = [
        {"run": "test", "name": "test"},
        {"run": "test1", "name": "test1", "dependancy": ["test"]},
        {"run": "test2", "name": "test2", "parameters": ["test", "test", "test"]},
    ]
    steps_to_mock = {"test": "test", "test1": "test1"}

    mock_steps(steps_to_mock)

    with pytest.raises(RuntimeError):
        _ = parse_steps(step_definitions)


def test_invalid_definition(mock_steps):
    step_definitions = [
        {"name": "test"},
        {"run": "test1", "name": "test1", "dependancy": ["test"]},
        {"run": "test2", "name": "test2", "parameters": ["test", "test", "test"]},
    ]
    steps_to_mock = {"test": "test", "test1": "test1"}

    mock_steps(steps_to_mock)

    with pytest.raises(RuntimeError):
        _ = parse_steps(step_definitions)
