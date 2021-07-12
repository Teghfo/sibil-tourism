from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import HandProductCartItem


@login_required(login_url='user-view', redirect_field_name='next')
def hand_product_show_cart(request):
    cart_items = request.cart.cart_items.all()
    #TODO function can calculate shipping
    shipping = 0
    if cart_items:
        shipping = 10000

    total = request.cart.cart_summation + shipping
    context = {
        'cart_items': cart_items,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'order/base_order.html', context)


@login_required(login_url='user-view', redirect_field_name='next')
def hand_product_add_cart(request, product_id):
    #TODO check existance!
    try:
        if request.cart.cart_items.filter(product__id=product_id).exists():
            cart_item = request.cart.cart_items.all().get(product__id=product_id)
            cart_item.qty += 1
            cart_item.save()
        else:
            HandProductCartItem.objects.create(user_cart=request.cart, product_id=product_id, qty=1)
        messages.success(request, "added successfully!")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('show_cart')