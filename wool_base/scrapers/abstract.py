from abc import ABC, abstractmethod
from wool_base.models import Product, Offer, Shop


class AbstractShopScraper(ABC):
    """
    Abstract interface for scrapers.
    """

    def __init__(self, shop: Shop):
        self.shop = shop

    @abstractmethod
    def fetch_offer(self, product: Product) -> Offer | None:
        raise NotImplementedError
