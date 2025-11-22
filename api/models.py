from django.db import models

class Product(models.Model) :
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    product_amount = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_number)

