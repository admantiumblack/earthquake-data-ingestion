from extraction.source import APIDataSource
from utils.path_parser import resolve_path
import yaml


def get_data_source(source: str | dict[str, str | dict]):
    if isinstance(source, str):
        source_file = resolve_path(f"extraction/api_sources/{source}.yaml")
        with open(source_file, "r") as f:
            source = yaml.safe_load(f)

    return APIDataSource(**source)
