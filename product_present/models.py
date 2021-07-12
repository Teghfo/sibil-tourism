from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import HandProductSuplier
from .validators import file_size_validator

User = get_user_model()


class HandProductCat(models.Model):
    name = models.CharField(max_length=255)
    cat = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HandProductCity(models.Model):
    city = models.CharField(max_length = 255)

    def __str__(self):
        return self.city


class HandProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(HandProductCat , on_delete=models.CASCADE, related_name='hand_product')
    city = models.ForeignKey(HandProductCity, on_delete=models.CASCADE, related_name="hand_product")
    supplier = models.ForeignKey(HandProductSuplier, on_delete=models.CASCADE)
    price = models.IntegerField()
    img_one = models.ImageField(upload_to="hand_product/")
    img_two = models.ImageField(upload_to="hand_product/", null=True, blank=True)
    img_three = models.ImageField(upload_to="hand_product/", null=True, blank=True)
    video_description = models.FileField(upload_to='hand_product_video/', null=True, blank=True, validators=[file_size_validator])
    slug = models.SlugField(unique=True, null=True, blank=True)
    active = models.BooleanField(default=False)
    discount_rate = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def price_after_discount(self):
        new_price = int(self.price - (self.price * self.discount_rate)/100)
        return new_price


class HandProductComment(models.Model):
    hand_product= models.ForeignKey(HandProduct, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hand_product_comments")
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)

    def __str__(self):
        return f"comment by {self.user.email}"

    class Meta:
        permissions = [('can_delete_comment', 'Can Delete Comment')]
