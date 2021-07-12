from django.urls import path

from .views import hand_product_show_cart, hand_product_add_cart

urlpatterns = [
    path('show-cart/', hand_product_show_cart, name='show_cart'),
    path('add-cart/<int:product_id>', hand_product_add_cart, name='add_cart'),
]