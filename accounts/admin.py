from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Informations'), {'fields': ('name', 'phone','age','otp')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff','is_teacher','is_student',
                                       'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_staff'),   
        }),
    )
    list_display = ('id', 'email','name','is_teacher','is_student', 'is_staff')
    list_display_links = ('id', 'email')
    search_fields = ('email','name')
    ordering = ('id', 'email')