from django.core.management.base import BaseCommand

from wool_base.models import Shop, Product, Offer
from wool_base.scrapers.wollplatz_scraper import WollplatzScraper


class Command(BaseCommand):
    help = 'Scrape products from desired shops'

    PRODUCTS = [
        {'brand': 'DMC', 'name': 'Natura XL'},
        {'brand': 'Drops', 'name': 'Safran'},
        {'brand': 'Drops', 'name': 'Baby Merino Mix'},
        {'brand': 'Hahn', 'name': 'Alpacca Speciale'},
        {'brand': 'Stylecraft', 'name': 'Special DK'},
    ]

    SHOPS = [
        {
            'name': 'Wollplatz',
            'base_url': 'https://www.wollplatz.de',
            'scraper_class': WollplatzScraper,
        },
    ]

    def handle(self, *args, **options):
        total_created = 0
        total_updated = 0
        
        for shop_config in self.SHOPS:
            shop, _ = Shop.objects.get_or_create(
                name=shop_config['name'],
                defaults={'base_url': shop_config['base_url']}
            )
            
            scraper = shop_config['scraper_class'](shop)
            
            self.stdout.write(f'\nProcessing shop: {shop.name}')
            
            for product_data in self.PRODUCTS:
                product, _ = Product.objects.get_or_create(
                    brand=product_data['brand'],
                    name=product_data['name']
                )
                
                offer = scraper.scrape_offer(product)
                
                if offer:
                    offer_obj, created = Offer.objects.update_or_create(
                        product=product,
                        shop=shop,
                        defaults={
                            'price': offer.price,
                            'availability': offer.availability,
                            'needle_size': offer.needle_size,
                            'composition': offer.composition,
                            'url': offer.url,
                        }
                    )
                    if created:
                        total_created += 1
                    else:
                        total_updated += 1
                    self.stdout.write(f'DONE {product.brand} {product.name}')
                else:
                    self.stdout.write(f'ERROR {product.brand} {product.name} - not found')
        
        self.stdout.write(f'Total: created: {total_created}, updated: {total_updated} offers for desired products')
