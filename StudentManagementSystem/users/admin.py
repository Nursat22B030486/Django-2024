from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')

    # Fields to edit in the admin detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to show when creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    # Search and ordering
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)

# Register the custom User model with the custom admin
admin.site.register(User, UserAdmin)
