from django.db import models


# Industry Model
class Industry(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    industry = models.ForeignKey(
        "Industry", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=150)
    descriptions = models.TextField()
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    color = models.ForeignKey(
        "ProductColor", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title
