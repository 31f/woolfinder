import logging
import re
import time
from decimal import Decimal

import cloudscraper
from bs4 import BeautifulSoup

from wool_base.scrapers.abstract import AbstractShopScraper

logger = logging.getLogger(__name__)


class WollplatzScraper(AbstractShopScraper):
    def __init__(self, shop):
        super().__init__(shop)
        self.session = cloudscraper.create_scraper()

    def _build_product_url(self, product):
        """
        As a shortcut we assume if there is a product, then it has a page like /wolle/brand/brand-name
        Better but more complex approach will be run to use /search functionality.
        """
        brand_lower = product.brand.lower()
        name_lower = product.name.lower().replace(' ', '-')
        url = f"{self.base_url}/wolle/{brand_lower}/{brand_lower}-{name_lower}"
        return url

    def _extract_price(self, soup):
        for selector in [{'class': re.compile(r'price', re.I)}, {'class': re.compile(r'preis', re.I)}]:
            elem = soup.find(['span', 'div'], selector)
            if elem:
                text = elem.get_text(strip=True)
                match = re.search(r'(\d+[.,]\d+)', text.replace('.', '').replace(',', '.'))
                if match:
                    try:
                        return Decimal(match.group(1))
                    except:
                        continue
        return None

    def _extract_availability(self, soup):
        text = soup.get_text().lower()
        if any(word in text for word in ['auf lager', 'verfügbar', 'lieferbar']):
            return True
        if any(word in text for word in ['nicht verfügbar', 'ausverkauft']):
            return False
        return True

    def _extract_needle_size(self, soup):
        for td in soup.find_all('td'):
            if td.get_text(strip=True).lower() == 'nadelstärke':
                next_td = td.find_next_sibling('td')
                if next_td:
                    needle_size = next_td.get_text(strip=True)
                    return needle_size
        logger.warning("Needle size not found in table")
        return None

    def _extract_composition(self, soup):
        for td in soup.find_all('td'):
            text = td.get_text(strip=True).lower()
            if text in ['zusammensetzung', 'zusammenstellung']:
                next_td = td.find_next_sibling('td')
                if next_td:
                    composition = next_td.get_text(strip=True)
                    return composition[:255]
        logger.warning("Composition not found in table")
        return None

    def scrape_offer(self, product):
        product_url = self._build_product_url(product)
        logger.info(f"Fetching product: {product.brand} {product.name} from {product_url}")
        
        try:
            time.sleep(2)
            response = self.session.get(product_url, timeout=10)
            
            if response.status_code == 403:
                logger.error(f"403 Forbidden - Access denied to: {product_url}")
                return None
            
            if response.status_code == 404:
                logger.error(f"404 Not Found - Product page does not exist: {product_url}")
                return None
            
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            price = self._extract_price(soup)
            availability = self._extract_availability(soup)
            needle_size = self._extract_needle_size(soup)
            composition = self._extract_composition(soup)
            
            offer = self.prepare_offer(
                product=product,
                price=price,
                availability=availability,
                needle_size=needle_size,
                composition=composition,
                url=product_url,
            )
            
            logger.info(f"Successfully scraped {product.brand} {product.name}: "
                        f"price={price}, available={availability}, "
                        f"needle={needle_size}, composition={composition}")
            return offer
        except Exception as e:
            logger.error(f"Error scraping {product.brand} {product.name}: {e}")
            return None
