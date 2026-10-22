"""The current 5-minute real-time LMP from ISO-NE web services.

One call per location. ISO-NE publishes each 5-minute interval's price a
minute or two after the interval starts, so "current" is the latest
interval it has priced.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import NamedTuple

import requests
from requests.auth import HTTPBasicAuth

ISONE_NAMESPACE = {"ns": "http://WEBSERV.iso-ne.com"}
CURRENT_URL = (
    "https://webservices.iso-ne.com/api/v1.1/fiveminutelmp/current/location/{location}"
)
TIMEOUT_S = 15


class FiveMinuteLmp(NamedTuple):
    """One 5-minute interval's locational marginal price at one node: the
    interval's start (unix seconds; the utc.seconds format is outside this
    snapshot's closure) and the total LMP in USD/MWh. Interior to the
    fetch; latest.price is the boundary form."""

    begin_s: int
    lmp_usd_per_mwh: float


class IsoneClient:
    """Fetches the current 5-minute LMP for one location with basic auth."""

    def __init__(self, user: str, password: str, location_id: str) -> None:
        self.auth = HTTPBasicAuth(user, password)
        self.location_id = location_id

    def current(self) -> FiveMinuteLmp:
        """The latest priced 5-minute interval at the location."""
        url = CURRENT_URL.format(location=self.location_id)
        response = requests.get(url, auth=self.auth, timeout=TIMEOUT_S)
        response.raise_for_status()
        return parse_current(response.text, self.location_id)


def parse_current(xml_text: str, location_id: str) -> FiveMinuteLmp:
    """The FiveMinuteLmp in a `fiveminutelmp/current` response."""
    root = ET.fromstring(xml_text)
    location = root.find("ns:Location", ISONE_NAMESPACE)
    if location is None or location.attrib.get("LocId") != location_id:
        raise ValueError(f"ISO-NE FiveMinLmp is not for location {location_id}")
    begin = root.find("ns:BeginDate", ISONE_NAMESPACE)
    total = root.find("ns:LmpTotal", ISONE_NAMESPACE)
    if begin is None or begin.text is None or total is None or total.text is None:
        raise ValueError("ISO-NE FiveMinLmp without BeginDate or LmpTotal")
    begin_dt = datetime.strptime(begin.text, "%Y-%m-%dT%H:%M:%S.%f%z")
    return FiveMinuteLmp(int(begin_dt.timestamp()), float(total.text))
