from typing import TypedDict


class TrafficPayload(TypedDict):
    country: str
    year: int
    rate: float
