from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
