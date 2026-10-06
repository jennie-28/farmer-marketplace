from django.db import models


class Farmer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer.name} - {self.product.product_name}"