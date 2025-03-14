import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from dotenv import load_dotenv
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator
from dlt.sources.helpers.rest_client import RESTClient
import os
from datetime import datetime

##############################
# Load matches before and after this day to their own tables
##############################

# env variables
load_dotenv()
api_key = os.getenv("API_KEY")

# build path for matches in the past month, excluding today to avoid not complete matches
monthAgo = datetime.now().replace(month=datetime.now().month-1).strftime('%Y-%m-%d')
yesterday = datetime.now().replace(day=datetime.now().day-1).strftime('%Y-%m-%d')
pastMonthMatchesPath = "matches-by-date?date=lt." + yesterday + "&date=gt." + monthAgo


### source ###
@dlt.source
def tennis_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://tennis.sportdevs.com/",
            "headers": {
                "Authorization": "Bearer " + api_key
            }
        },
        "resource_defaults": {
            "write_disposition": "replace"
        },
        "resources": [
            {
                "name": "past_month_matches",
                "endpoint": {
                    "path": pastMonthMatchesPath
                }
            },
            {
                "name": "leagues",
                "endpoint": {
                    "path": "leagues"
                }
            },
            {
                "name": "standings",
                "endpoint": {
                    "path": "standings"
                }
            }
        ],
    }

    yield from rest_api_resources(config)

def load_tennis() -> None:
    pipeline = dlt.pipeline(
        pipeline_name='rest_api_tennis',
        destination=dlt.destinations.duckdb("/data/tennisdb.duckdb"),
        dataset_name='tennis_stg',
        dev_mode=False
    )

    load_info = pipeline.run(tennis_source())
    print(load_info)



if __name__ == '__main__':
    load_tennis()