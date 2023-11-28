import argparse
import os
from datetime import datetime
from extraction import get_earthquake_data_source

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="earthquake_ingestion",
        description="ingestion layer for USGS earthquake API",
    )
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    parser.add_argument("-b", "--bucket", default=os.environ.get("DEFAULT_BUCKET"))
    parser.add_argument(
        "-f", "--format", default="parquet", choices=["parquet", "csv", "excel"]
    )
    parser.add_argument("-n", "--name", default=f"{datetime.now()}")
    
    api_source = get_earthquake_data_source()