from tap_orbit.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()


class MembersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "members"
    KEY_PROPERTIES = ["id"]

    def response_key(self):
        return "data"

    @property
    def path(self):
        return "/members"

    @property
    def api_method(self):
        return "GET"
