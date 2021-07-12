from django.contrib import admin

from . import models


class HandProductModelAdmin(admin.ModelAdmin):
    exclude = ['slug']

    def get_exclude(self, request, obj=None):
        """
        Hook for specifying exclude.
        """
        if request.user.is_superuser:
            return self.exclude
        else:
            return self.exclude + ['supplier', 'active']

    def save_model(self, request, obj, form, change):
        if not form.fields.get('supplier', None):
            obj.supplier = request.user.hand_product_suplier
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(supplier__user=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier.user != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier.user != request.user:
            return False
        return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.supplier.user != request.user:
            return False
        return True


admin.site.register(models.HandProduct, HandProductModelAdmin)
admin.site.register(models.HandProductCity)
admin.site.register(models.HandProductCat)
admin.site.register(models.HandProductComment)
