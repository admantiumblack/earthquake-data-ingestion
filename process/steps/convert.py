import pandas as pd
from process.steps import pipeline_step


@pipeline_step
def to_dataframe(data):
    dataframe = pd.from_dict(data)
    return dataframe
