from django.db import models
from accounts.models import User


class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    like_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images',null=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Products"
        ordering = ["like_count"]

    def __str__(self):
        return self.name
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
