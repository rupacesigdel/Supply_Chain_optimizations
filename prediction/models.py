from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    reorder_level = models.IntegerField()
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Inventory"

class SalesData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)  # Add default value
    promotion = models.BooleanField(default=False)
    season = models.CharField(max_length=20, choices=[
        ('Winter', 'Winter'),
        ('Spring', 'Spring'), 
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn')
    ])
    sales_quantity = models.IntegerField()

class ShipmentData(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    dispatch_date = models.DateField()
    expected_arrival = models.DateField()
    actual_arrival = models.DateField(null=True, blank=True)
    traffic_conditions = models.CharField(max_length=20, choices=[
        ('Light', 'Light'),
        ('Moderate', 'Moderate'),
        ('Heavy', 'Heavy'),
        ('Severe', 'Severe')
    ])
    weather_conditions = models.CharField(max_length=20, choices=[
        ('Clear', 'Clear'),
        ('Rainy', 'Rainy'),
        ('Snowy', 'Snowy'),
        ('Stormy', 'Stormy')
    ])