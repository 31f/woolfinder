from django.test import TestCase

from wool_base.models import Shop, Product, Offer


class OfferModelTest(TestCase):
    def test_create_offer_model(self):
        shop = Shop.objects.create(
            name='Wollplatz',
            base_url='https://www.wollplatz.de'
        )
        product = Product.objects.create(
            brand='DMC',
            name='Natura XL'
        )
        offer = Offer.objects.create(
            product=product,
            shop=shop,
            price=12.99,
            availability=True,
            needle_size='4-5 mm',
            composition='100% Baumwolle',
            url='https://www.wollplatz.de/wolle/dmc-natura-xl'
        )
        
        self.assertEqual(offer.price, 12.99)
        self.assertEqual(offer.availability, True)
        self.assertEqual(offer.needle_size, '4-5 mm')
        self.assertEqual(offer.composition, '100% Baumwolle')
        self.assertEqual(offer.product.brand, 'DMC')
        self.assertEqual(offer.product.name, 'Natura XL')
        self.assertEqual(offer.shop.name, 'Wollplatz')

