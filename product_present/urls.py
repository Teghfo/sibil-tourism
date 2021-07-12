from django.urls import path

from .views import (HandProductListView, HandProductDetailView,
                    CommentFormView, delete_comment_view, index_summation_celery)

urlpatterns = [
    path('handproducts/', HandProductListView.as_view(), name='hand-product-list'),
    path('handproduct/<str:slug>/', HandProductDetailView.as_view(), name='hand-product-detail'),
    path('commnet/<int:id>/', CommentFormView.as_view(), name='comment-change'),
    # path('comment_delete/<int:id>/',delete_comment_view, name="comment-delete" )
    # path('comment_delete/<int:id>/',CommentFormView.as_view(), name="comment-delete" )
    path('celery/',index_summation_celery, name="celery" )
]