from tap_orbit.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()


class ActivitiesStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "activities"
    KEY_PROPERTIES = ["id"]

    def response_key(self):
        return "data"

    @property
    def path(self):
        return "/activities"

    @property
    def api_method(self):
        return "GET"
