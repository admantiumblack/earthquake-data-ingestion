from extraction.source import APIDataSource
import os


def get_earthquake_data_source():
    url = os.environ['EARTHQUAKE_URL']
    return APIDataSource(url)