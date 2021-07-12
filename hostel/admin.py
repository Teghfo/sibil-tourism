from django.contrib import admin

from .models import HostelCategory, HostImage, HostAddress, Host, HostComment, HostStateAddress


class HostImageInline(admin.TabularInline):
    model = HostImage


class HostAddressInline(admin.TabularInline):
    model = HostAddress


class HostCommentInline(admin.TabularInline):
    model = HostComment


@admin.register(Host)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        HostImageInline,
        HostCommentInline,
        HostAddressInline
    ]


admin.site.register(HostelCategory)
admin.site.register(HostStateAddress)