from django.db import models

class ShipmentData(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    dispatch_date = models.DateTimeField()
    expected_arrival_date = models.DateTimeField()
    traffic_conditions = models.CharField(max_length=100)
    weather_conditions = models.CharField(max_length=100)
    actual_arrival_date = models.DateTimeField(null=True, blank=True)

class SalesData(models.Model):
    product_name = models.CharField(max_length=255)
    sales_date = models.DateTimeField()
    sales_quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.BooleanField()
    season = models.CharField(max_length=100)
