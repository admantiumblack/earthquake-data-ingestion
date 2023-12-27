import json
from cerberus import Validator
from utils.path_parser import resolve_path


def create_validator(schema: str | dict):
    if isinstance(schema, str):
        file_name = resolve_path(f"validation/schema/{schema}.json")
        with open(file_name, "r") as f:
            schema = json.load(f)
    validator = Validator(schema)
    validator.allow_unknown = True
    return validator
