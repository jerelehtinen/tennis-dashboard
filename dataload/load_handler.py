"""
This load handler class is meant to be generic and reusable for different API endpoints from SportDevs.
SportDevs API is a REST API that provides tennis data, including matches, leagues, and standings.
It has tricky pagination which is why dlt for example was difficult to use.
"""
import os
from pydantic import BaseModel
from typing import ClassVar, Optional
from dotenv import load_dotenv
from urllib.parse import urljoin
import requests
import pandas as pd
import duckdb
import logging
import time

logger = logging.getLogger("load_handler")
load_dotenv()


class LoadHandler(BaseModel):
    """
    A class to handle loading data from a given API endpoint.
    All SportDevs API endpoints support limit & offset pagination so that is used here. 
    """
    api_endpoint: str
    target_schema: str
    target_table: str
    params: Optional[dict] = {}
    headers: Optional[dict] = {}
    response_data: Optional[list] = []
    limit: int

    API_BASE_URL: ClassVar[str] = os.getenv("API_URL")
    DB_CONNECTION: ClassVar[str] = os.getenv("DB_CONNECTION")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # fixed values for all endpoints
        self.headers["Authorization"] = "Bearer " + os.getenv("API_KEY")
        self.headers["Content-Type"] = "application/json" 
        self.headers["Connection"] = "keep-alive"


    def load_data_to_db(self):
        """
        Fetch data from given API endpoint. 
        All calls are considered as full loads, so looping through pages until API returns empty response.
        TODO: add support for delta loads
        """
        full_url = urljoin(self.API_BASE_URL, self.api_endpoint)

        api_returned_data = True
        api_errored = False
        offset = 0
        while api_returned_data and not api_errored:
            offset += self.limit
            self.params["limit"] = self.limit
            self.params["offset"] = offset

            response = requests.get(
                full_url,
                headers=self.headers,
                params=self.params
            )
            data = response.json()

            if not data:
                api_returned_data = False
                logger.info(f"API returned no more data for endpoint {self.api_endpoint}. Jumping out of loop.")
            elif response.status_code != 200:
                api_errored = True
                logger.error(f"Error fetching data from {self.api_endpoint}: {response.status_code} - {response.text}")
                logger.error("Stopping execution.")
                raise Exception(f"Error fetching data from {self.api_endpoint}: {response.status_code} - {response.text}")
            else:
                self.response_data.extend(data)
                time.sleep(0.2)  # 200ms delay between requests to avoid hitting API rate limits
                logger.info(f"Fetched {len(data)} records from {self.api_endpoint} with offset {offset}")

        # convert data to pandas DataFrame and save to duckdb
        logger.info(f"Saving {len(self.response_data)} records to {self.target_schema}.{self.target_table}")
        df = pd.DataFrame(self.response_data)
        conn = duckdb.connect(self.DB_CONNECTION)
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {self.target_schema}")
        conn.execute(f"CREATE OR REPLACE TABLE {self.target_schema}.{self.target_table} AS SELECT * FROM df")



if __name__ == '__main__':
    load_handler = LoadHandler(
        api_endpoint="leagues",
        limit=50,
        target_schema="tennis_stg",
        target_table="leagues"
    )

    load_handler.load_data_to_db()