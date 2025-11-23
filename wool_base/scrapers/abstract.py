from abc import ABC, abstractmethod

from wool_base.models import Product, Offer, Shop


class AbstractShopScraper(ABC):
    """
    Abstract interface for scrapers.
    """

    def __init__(self, shop: Shop):
        self.shop = shop
        self.base_url = shop.base_url or ''

    def prepare_offer(self, product, price=None, availability=False, 
                     needle_size=None, composition=None, url=None):
        return Offer(
            product=product,
            shop=self.shop,
            price=price,
            availability=availability,
            needle_size=needle_size,
            composition=composition,
            url=url,
        )

    @abstractmethod
    def scrape_offer(self, product: Product) -> Offer | None:
        raise NotImplementedError
