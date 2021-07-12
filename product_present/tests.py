from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django import forms

from .models import HandProduct
from .views import HandProductDetailView
from .forms import CommentForm

# Model Test #


class HandProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product = HandProduct(name="ru farshi")

    def test_hand_product_name_label(self):
        name = self.product._meta.get_field('name').verbose_name
        self.assertEqual(name, 'name')

    def test_hand_product_name_max_length(self):
        name_max_length = self.product._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 255)

# Form test #


class CommentFormTest(TestCase):
    def setUp(self) -> None:
        self.form = CommentForm()

    def test_rate_field_label(self):
        rate_label = self.form.fields['rate'].label
        self.assertEqual(rate_label, "ریت")

    def test_rate_field_data_type(self):
        self.assertTrue(isinstance(self.form.fields['rate'], forms.IntegerField))

    def test_rate_field_max_min_val(self):
        form_invalid_max = CommentForm(data={'rate': 6})
        self.assertFalse(form_invalid_max.is_valid())
        form_invalid_min = CommentForm(data={'rate': -1})
        self.assertFalse(form_invalid_min.is_valid())
        form_valid_min = CommentForm(data={'rate': 0})
        self.assertTrue(form_valid_min.is_valid())
        form_valid_max = CommentForm(data={'rate': 5})
        self.assertTrue(form_valid_max.is_valid())

# view test #


class HandProductViewTest(TestCase):

    fixtures = ['hand_products']

    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()

    def test_url_hand_product_detail(self):
        product = HandProduct.objects.get(pk=1)
        url = reverse('hand-product-detail', kwargs={"slug":product.slug})
        # self.assertEqual(url, f'/product_present/handproduct/{product.slug}/')

    # def test_hand_product_detail(self):
    #     product = HandProduct.objects.get(pk=1)
    #     response = self.client.get(reverse('hand-product-detail', kwargs={"slug":product.slug}))
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'product_present/product_detail.html')
    #     self.assertContains(response, "Sibil")

    def test_hand_product_detail(self):
        product = HandProduct.objects.get(pk=1)
        request = self.factory.get(reverse('hand-product-detail', kwargs={"slug":product.slug}))

        request.user = AnonymousUser()
        response = HandProductDetailView.as_view()(request, slug=product.slug)
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'product_present/product_detail.html')
        self.assertContains(response, "Sibil")