import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from dotenv import load_dotenv
import os
from datetime import datetime

##############################
# Load matches before and after this day to their own tables
##############################

# env variables
load_dotenv()
api_key = os.getenv("API_KEY")

today = datetime.now().strftime('%Y-%m-%d')
futureMatchesPath = "matches-by-date?date=gt." + today
pastMatchesPath = "matches-by-date?date=lt." + today

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
        "resources": [
            {
                "name": "future_matches_by_date",
                "endpoint": {
                    "path": futureMatchesPath
                }
            },
            {
                "name": "past_matches_by_date",
                "endpoint": {
                    "path": pastMatchesPath
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