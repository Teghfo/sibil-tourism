import debug_toolbar
from datetime import timedelta
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    # if request.user.is_authenticated and not cache.get(request.user, None):
    #     cache.set(request.user, request.cart.cart_items_cardinality)
    return render(request, "index.html",{})


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('', index, name="home"),
    path('profile/',include("user.urls")),
    path('product_present/',include("product_present.urls")),
    path("accounts/" , include("django.contrib.auth.urls")),
    path("order/" , include("order.urls")),
    path("host-api/", include("hostel.urls"), name="hostel"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
