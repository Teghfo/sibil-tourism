from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView

from .models import HandProduct, HandProductComment
from .forms import CommentForm
from .tasks import summation

class HandProductListView(ListView):
    model = HandProduct
    template_name = "product_present/product_list.html"
    context_object_name = 'hand_products'
    paginate_by = 3
    # queryset = HandProduct.objects.filter(category__name="خوراکی")

    def get_queryset(self):
        query_set = super().get_queryset().filter(active=True)
        if self.request.GET.get('q', None):
            query_set = query_set.filter(name__contains=self.request.GET.get('q', None))
        if self.request.GET.get('min_price', None):
            query_set = query_set.filter(price__gt=int(self.request.GET.get('min_price', None)))
        if self.request.GET.get('max_price', None):
            query_set = query_set.filter(price__lt=int(self.request.GET.get('max_price', None)))

        return query_set

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return int(self.request.GET.get('paginate_by', self.paginate_by))


class HandProductDetailView(DetailView):
    model = HandProduct
    template_name = "product_present/product_detail.html"
    context_object_name = 'hand_product'


class CommentFormView(View):

    @method_decorator(login_required(login_url="/profile/user/"))
    def dispatch(self, request, *args, **kwargs):
        self.hand_product = get_object_or_404(HandProduct, id = self.kwargs["id"])
        if request.user.hand_product_comments.all().filter(hand_product=self.hand_product).exists():
            self.comment_instance = request.user.hand_product_comments.all().get(hand_product=self.hand_product)
        else:
            self.comment_instance = None
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        if self.comment_instance:
            form = CommentForm(instance = self.comment_instance)
        else:
            form = CommentForm()
        return render(request, "product_present/comment_change.html", {"form":form , "id":id})

    def post(self, request, id):
        if self.comment_instance:
            form = CommentForm(data=request.POST, instance = self.comment_instance)
        else:
            form = CommentForm(request.POST)
            form.instance.user = request.user
            form.instance.hand_product = self.hand_product
        if form.is_valid():
            try:
                form.save()
                return HttpResponse("damet garm")
            except Exception as e:
                raise IntegrityError(e)
        return render(request, "product_present/comment_change.html", {"form":form, "id":id})

    def delete(self, request, id):

        if self.comment_instance.user == request.user:
            self.comment_instance.delete()
            return HttpResponse("be khubi va khoshi hazfid!")
        else:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")


def delete_comment_view(request, id):
    comment = get_object_or_404(HandProductComment, id = id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponse("be khubi va khoshi hazfid!")
    else:
        return HttpResponseForbidden("<h1>403 Forbidden</h1>")


def index_summation_celery(request):
    result = summation.delay(1, 5)
    return HttpResponse(f"hello celery {result}")