from django.db import models
from django.contrib.auth import get_user_model

from product_present.models import HandProduct

User = get_user_model()


class HandProductCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    @property
    def cart_items_cardinality(self):
        return self.cart_items.count()

    @property
    def cart_summation(self):
        cart_items = self.cart_items.select_related('product')
        sum_prices = 0
        for item in cart_items:
            sum_prices += (item.product.price_after_discount() * item.qty)
        return sum_prices

    def __str__(self):
        return self.user.email


class HandProductCartItem(models.Model):

    CHOICE_CART_ITEM_STATUS = (
        ('O', 'OPEN'),
        ('P', 'PAYED'),
        ('F', 'FAILED')
    )

    user_cart = models.ForeignKey(HandProductCart, related_name='cart_items',on_delete=models.CASCADE)
    product = models.ForeignKey(HandProduct, on_delete=models.CASCADE)
    qty = models.SmallIntegerField()
    status = models.CharField(default='O', max_length=1, choices=CHOICE_CART_ITEM_STATUS)

    @property
    def product_sum_price(self):
        return self.product.price_after_discount() * self.qty

    def __str__(self):
        return f"{self.user_cart.user.email} - {self.product.name}"
