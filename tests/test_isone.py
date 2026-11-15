"""Parsing ISO-NE's fiveminutelmp/current response."""

from datetime import datetime

import pytest

from gwmm.gate import WholesaleLmp
from gwmm.isone import parse_current

SAMPLE = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<FiveMinLmp xmlns="http://WEBSERV.iso-ne.com">'
    "<BeginDate>2026-10-22T10:40:00.000-04:00</BeginDate>"
    '<Location LocId="43790" LocType="NETWORK NODE">LD.KEENE_RD44  </Location>'
    "<LmpTotal>31.34</LmpTotal><EnergyComponent>32.12</EnergyComponent>"
    "<CongestionComponent>0.04</CongestionComponent>"
    "<LossComponent>-0.82</LossComponent></FiveMinLmp>"
)


def test_parse_current() -> None:
    interval = parse_current(SAMPLE, "43790")
    assert interval.lmp == WholesaleLmp(32_120, 40, -820)
    assert interval.lmp.total_x1000 == 31_340
    begin = datetime.fromisoformat("2026-10-22T10:40:00-04:00")
    assert interval.begin_s == int(begin.timestamp())


def test_wrong_location_is_an_error() -> None:
    with pytest.raises(ValueError):
        parse_current(SAMPLE, "4001")


def test_a_missing_component_is_an_error() -> None:
    with pytest.raises(ValueError, match="LossComponent"):
        parse_current(
            SAMPLE.replace("<LossComponent>-0.82</LossComponent>", ""), "43790"
        )
