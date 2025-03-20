from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} (${self.price})"

class RawRP(models.Model):
    labels = models.CharField(max_length=50)
    data = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.labels}"

class Purchase(models.Model):
    customer_full_name = models.CharField(max_length=64)
    item = models.ForeignKey(to=Item, on_delete=models.RESTRICT)
    PAYMENT_METHODS = [
        ("CC", "Credit card"),
        ("DC", "Debit card"),
        ("ET", "Ethereum"),
        ("BC", "Bitcoin"),
    ]
    payment_method = models.CharField(max_length=2, default="CC", choices=PAYMENT_METHODS)
    time = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{self.customer_full_name}, {self.payment_method} ({self.item.name})"
