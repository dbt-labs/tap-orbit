import singer
import singer.utils
import singer.metrics

from tap_orbit.state import incorporate, save_state

from tap_framework.streams import BaseStream as base
from tap_orbit.cache import stream_cache


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ["id"]
    CACHE = False

    def sync_paginated(self, path, method):
        table = self.TABLE
        page_number = 1

        while True:
            response = self.client.make_request(path, method, page_number)

            transformed = self.get_stream_data(response)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, transformed)
                counter.increment(len(transformed))

            if self.CACHE:
                stream_cache[table].extend(transformed)

            data = response.get("data", [])

            if len(data) > 0:
                page_number += 1
            else:
                break

    def sync_data(self):
        table = self.TABLE
        LOGGER.info("Syncing data for {}".format(table))
        self.sync_paginated(self.path, self.api_method)

        return self.state

    def get_stream_data(self, response):
        transformed = []

        for record in response[self.response_key()]:
            record = self.transform_record(record)
            transformed.append(record)

        return transformed
