import argparse
import os
from datetime import datetime
from extraction import get_data_source
from validation import create_validator
from process import Pipeline
from repository import GCSRepository


def main(arguments):
    api_source = get_data_source(arguments.type)
    validator = create_validator(arguments.type)
    api_source.validator = validator
    parameter = api_source.construct_parameter(arguments)
    data = api_source.query_source(parameter).validate().clean_data
    pipeline = Pipeline(arguments.type)
    result = pipeline.run(data)
    repository = GCSRepository(arguments.bucket)
    repository.save(result, arguments.name, arguments.format)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="earthquake_ingestion",
        description="ingestion layer for USGS earthquake API",
    )
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    parser.add_argument("-t", "--type", default="earthquake")
    parser.add_argument("-b", "--bucket", default=os.environ.get("DEFAULT_BUCKET"))
    parser.add_argument(
        "-f", "--format", default="parquet", choices=["parquet", "csv", "excel"]
    )
    parser.add_argument("-n", "--name", default=f"{datetime.now()}")
    parser.add_argument("-s", "--storage", default="gcs", choices=["gcs", "s3"])

    main(parser.parse_args())
