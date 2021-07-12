from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy

from .forms import LoginForm, SuplierCreateForm, CustomPasswordChangeForm
from .models import HandProductSuplier, Profile
from .forms import CustomUserCreationForm

User = get_user_model()

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            # logout(request)
            return redirect('/')
        form = LoginForm()
        print(form.as_p())
        next_url = request.GET.get('next', '')
        context = {
            'form': form,
            'next_url': next_url
        }
        return render(request, 'user/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "login successfully!")
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                return redirect('/')
            else:
                return redirect('login')

#
# class SignUp(View):
#     def get(self, request):
#         form = CustomUserCreationForm()
#         context = {
#             'form': form
#         }
#
#         return render(request, 'signup.html', context)
#
#     def post(self, request):
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#
#         context = {
#             'form': form
#         }
#         return render(request, 'user/signup.html', context)
#
#
def logout_view(request):
    logout(request)
    return redirect('user-view')

#
@login_required(login_url='profile/user/')
# @permission_required('user.can_dance',  raise_exception=True)
def gher_umdan(request):
    if request.user.has_perm('user.can_dance'):
        return HttpResponse('Baba Karam!')
    return HttpResponse('raghs harameh!')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        if email:
            password = request.POST.get('password', None)
            if password:
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    if request.GET.get('next_url',None):
                        return redirect(request.GET.get('next_url'))
                    return redirect("home")
                else:
                    return HttpResponse("user pass eshtebah")
        else:
            return HttpResponse("email ro bezar")


def user_view(request):
    next_url = request.GET.get('next', '')
    return render(request, "user/user.html", { 'next_url': next_url})


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        if email:
            password = request.POST.get('password', None)
            repeated_passweord = request.POST.get('repeat_password', None)
            if password:
                if password == repeated_passweord:
                    try:
                        User.objects.create_user(email=email, password=password, phone=phone)
                        messages.success(request, "Register Successfully!")
                        return redirect('user-view')
                    except IntegrityError as e:
                        # return render(request, "user/error.html", {"message": e})
                        messages.error(request, f"{e}")
                        return redirect('user-view')
                else:
                    return HttpResponse("pass va tekraresh equal nistan")


@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(LoginRequiredMixin, View):
    login_url = "/profile/user/"
    def get(self, request):
        if Profile.objects.filter(user=request.user).exists():
            profile_object = request.user.profile
        else:
            profile_object = Profile.objects.create(user=request.user)

        context = {
            'profile_object': profile_object,
        }
        return render(request, 'user/profile.html', context)

    def post(self, request):
        return HttpResponse("in post")


class ProfileEdit(TemplateView):
    template_name = 'user/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_object'] = self.request.user
        return context


class RegisterSuplier(CreateView):
    model = HandProductSuplier
    form_class = SuplierCreateForm
    template_name = "user/create_supplier.html"
    success_url = "/profile/user/"

class ManageSuplierPageView(LoginRequiredMixin , View):
    login_url = "profile/user"

    def get(self, request):
        # TODO exception
        supplier = request.user.hand_product_suplier
        products = suplier.handproduct_set.all()
        context = {
            "supplier": supplier,
            "products": products,
        }
        return render(request, "user/manage_supplier_page.html", context)


class CustomChangePasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('user:password_change_ok')
    template_name = 'user/password_change_form.html'

def password_change_done(request):
    return render(request, "user/password_change_done.html", {})