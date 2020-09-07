import time
import requests
import singer
import zlib
import json
import base64


from tap_framework.client import BaseClient
from requests.auth import HTTPBasicAuth


LOGGER = singer.get_logger()
BASE_URL = "https://app.orbit.love/"


class OrbitClient(BaseClient):
    def __init__(self, config):
        super().__init__(config)

        self.user_agent = self.config.get("user_agent")
        self.api_key = self.config.get("api_key")
        self.workspace_id = self.config.get("workspace_id")

    def get_params(self, page_number):
        params = {
            "items": 500,
            "api_key": self.config.get("api_key"),
            "page": page_number,
        }
        return params

    def get_headers(self):
        ## As per Orbit docs
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
        return headers

    def get_authorization(self):
        pass

    def make_request(self, path, method, page_number, base_backoff=45):
        url = BASE_URL + self.workspace_id + path

        params = self.get_params(page_number)

        headers = self.get_headers()

        LOGGER.info("Making {} request to {}".format(method, url))

        response = requests.request(
            method, url, params=params, headers=headers, base_backoff=45
        )

        LOGGER.info("Received response ({}) from server".format(response.status_code))

        if response.status_code == 400:
            LOGGER.info("Got a 400, request was malformed")
            return None

        if response.status_code == 401:
            LOGGER.info("Got a 401, unauthorized request")
            return None

        if response.status_code == 429:
            LOGGER.info(
                "Got a 429, sleeping for {} seconds and trying again".format(
                    base_backoff
                )
            )
            time.sleep(base_backoff)
            return self.make_request(
                 path, method, page_number, base_backoff * 2
            )

        if response.status_code == 404:
            LOGGER.info("Got a 404, resource was not found")
            return None

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()
