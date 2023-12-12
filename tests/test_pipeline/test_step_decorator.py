import pytest
from process.steps.step_decorator import pipeline_step

def test_decorator():
    funct = lambda x: x
    decorated_funct = pipeline_step(funct)
    named_funct = decorated_funct(name='test', dependancy=[])

    assert named_funct.name == 'test'
    assert named_funct.dependancy == []
    assert named_funct == funct