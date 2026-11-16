"""The current 5-minute real-time LMP from ISO-NE web services.

One call per location. ISO-NE posts each 5-minute interval's price about
25 s after the interval begins, so "current" is the latest interval it
has posted, which the gate compares with the slot it wants.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal

import requests
from requests.auth import HTTPBasicAuth

from gwmm.gate import FiveMinuteLmp, WholesaleLmp

ISONE_NAMESPACE = {"ns": "http://WEBSERV.iso-ne.com"}
CURRENT_URL = (
    "https://webservices.iso-ne.com/api/v1.1/fiveminutelmp/current/location/{location}"
)
TIMEOUT_S = 15


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
    begin = text_of(root, "BeginDate")
    begin_dt = datetime.strptime(begin, "%Y-%m-%dT%H:%M:%S.%f%z")
    lmp = WholesaleLmp(
        energy_x1000=x1000(text_of(root, "EnergyComponent")),
        congestion_x1000=x1000(text_of(root, "CongestionComponent")),
        loss_x1000=x1000(text_of(root, "LossComponent")),
    )
    return FiveMinuteLmp(int(begin_dt.timestamp()), lmp)


def text_of(root: ET.Element, tag: str) -> str:
    """The text of the response's one `tag` element."""
    element = root.find(f"ns:{tag}", ISONE_NAMESPACE)
    if element is None or element.text is None:
        raise ValueError(f"ISO-NE FiveMinLmp without {tag}")
    return element.text


def x1000(usd_per_mwh: str) -> int:
    """A decimal USD/MWh amount as the price word's integer, times 1000."""
    return int((Decimal(usd_per_mwh) * 1000).to_integral_value())
