from django.contrib import messages
from django.contrib import admin

from .models import Profile, UserAddress, HandProductSuplier, HostelOwner
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active','is_superuser','phone',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('email', 'password', 'first_name')}),
        ('Permissions', {
         'fields': ('is_staff', 'is_active', 'user_permissions','is_superuser','groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'user_permissions', 'phone',)}
         ),
    )
    search_fields = ('is_staff',)
    ordering = ('email',)

#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone')
#     # exclude = ['image']
#     form = ProfileForm
#     list_editable = ('phone',)

    # def save_form(self, request, form, change):
    #     messages.add_message(request, messages.ERROR, 'SHALGHAM.')
    #     return super().save_form(request, form, change)

    # def get_form(self, request, obj=None, **kwargs):
    #     print(request.POST)
    #     kwargs['form'] = ProfileForm
    #     return super().get_form(request, obj, **kwargs)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(UserAddress)
admin.site.register(HandProductSuplier)
admin.site.register(HostelOwner)