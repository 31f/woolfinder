from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("brand", "name")

    def __str__(self):
        return f"{self.brand} {self.name}"


class Offer(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="offers",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2,
                                null=True, blank=True)
    currency = models.CharField(max_length=10, default="EUR")

    availability = models.BooleanField(default=False)
    needle_size = models.CharField(max_length=100, null=True, blank=True)
    composition = models.CharField(max_length=255, null=True, blank=True)

    url = models.URLField(null=True, blank=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "shop")

    def __str__(self):
        return f"{self.product} from {self.shop}"
