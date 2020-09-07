from tap_orbit.streams.activities import ActivitiesStream
from tap_orbit.streams.members import MembersStream

AVAILABLE_STREAMS = [
    ActivitiesStream,
    MembersStream,
]

__all__ = [
    "ActivitiesStream",
    "MembersStream",
]
