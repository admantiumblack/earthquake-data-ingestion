from extraction.source import APIDataSource
from utils.path_parser import resolve_path
import yaml


def get_data_source(source:str|dict[str, str|dict]):
    if isinstance(source, str):
        with open(resolve_path(f'extraction/api_sources/{source}.yaml'), 'r') as f:
            source = yaml.safe_load(f)
    
    return APIDataSource(**source)
