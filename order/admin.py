from django.contrib import admin

from .models import HandProductCart, HandProductCartItem


class CartItemInline(admin.TabularInline):
    model = HandProductCartItem


@admin.register(HandProductCart)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]



