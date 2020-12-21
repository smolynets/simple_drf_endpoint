from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    desription = models.TextField()
    number = models.IntegerField()
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name
