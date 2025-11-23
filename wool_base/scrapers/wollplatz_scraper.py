from __future__ import annotations

from typing import Optional


from wool_base.scrapers.abstract import AbstractShopScraper
from wool_base.models import Product, Offer


class WollplatzScraper(AbstractShopScraper):
    BASE_URL = "https://www.wollplatz.de"

    def __init__(self, shop):
        super().__init__(shop)

    def fetch_offer(self, product: Product) -> Optional[Offer]:
        pass
