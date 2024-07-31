from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User,
    Recipe,
    Tag,
    Ingredient
    )

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'is_staff', 'last_login']
    search_fields = ['email', 'name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ['last_login']

admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)