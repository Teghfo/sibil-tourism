from order.models import HandProductCart
from django.utils.deprecation import MiddlewareMixin


class CartMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        print("in pr req")
        assert hasattr(request, 'user'), "shalgham man bad az Auth middleweram"
        if request.user.is_authenticated:
            cart, status = HandProductCart.objects.get_or_create(user=request.user)
            request.cart = cart

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print("in pr view", view_func)

    def process_response(self, request, response):
        print(response)
        return response

    def process_exception(self, request, exception):
        print('hellllllo')
        return None