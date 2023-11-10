from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_property_owner', 'is_admin', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_property_owner', 'is_admin',)
    search_fields = ('email', 'is_property_owner', 'is_admin',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_property_owner', 'is_admin', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_property_owner', 'is_admin', 'is_staff', 'is_active'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('id', 'user', 'phone_number', 'photo')
    list_filter = ('id', 'user', 'phone_number',)
    search_fields = ('id', 'user', 'phone_number',)
    ordering = ('user',)
