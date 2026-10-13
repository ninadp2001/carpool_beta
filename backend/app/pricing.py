"""Every price is calculated here, on the server. The client never sends an amount."""
from dataclasses import dataclass

from .config import get_settings


@dataclass
class Quote:
    base: int
    tax: int
    total: int


def quote(base_paise: int) -> Quote:
    tax = round(base_paise * get_settings().gst_rate)
    return Quote(base=base_paise, tax=tax, total=base_paise + tax)
