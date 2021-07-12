from django.urls import path

from .views import (logout_view, login_view, signup, Login,
                    user_view, ProfileView, ProfileEdit, gher_umdan, RegisterSuplier, ManageSuplierPageView,
                    CustomChangePasswordView, password_change_done)

urlpatterns = [
    # path('login/', Login.as_view(), name='login'),
    # path('signup/', SignUp.as_view(), name='signup'),
    # path('logout/', logout_view, name='logout'),
    # path('gher/', gher_umdan, name='gher-umadan'),

    path('login/', login_view, name='login'),
    path('login_class/', Login.as_view(), name='login-class'),
    path('signup/', signup, name='signup'),
    path('user/', user_view, name='user-view'),
    path('logout/', logout_view, name='logout_view'),
    path('information/', ProfileView.as_view()),
    path('edit/', ProfileEdit.as_view(), name='edit'),
    path("gher_umadan/", gher_umdan),
    path("register_suplier/", RegisterSuplier.as_view()),
    path("suplier/", ManageSuplierPageView.as_view(), name="suplier-manage-page"),
    path("change_password/", CustomChangePasswordView.as_view(), name="change-password"),
    path("change_done/", password_change_done, name="password_change_ok"),
]
