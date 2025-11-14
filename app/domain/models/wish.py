from dataclasses import dataclass


@dataclass
class Wish:
    title: str
    link: str | None
    price_estimate: int | None
    notes: str | None
    is_booked: bool = False
