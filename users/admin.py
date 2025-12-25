from django.contrib import admin
from .models import NewUser, Profile
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name', 'last_name')
    list_filter = ('email', 'user_name', 'first_name', 'last_name', 'is_staff', 'is_active')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Personal', {'fields': ('about',)}),
    )
    formfields_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )


admin.site.register(NewUser, UserAdminConfig)

admin.site.register(Profile)
