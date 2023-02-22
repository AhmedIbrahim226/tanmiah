from django.contrib import admin
from .models import UserAuth, UserProfile
from django.contrib.auth.admin import UserAdmin

@admin.register(UserAuth)
class MyUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_superuser', 'is_staff', 'is_user', 'is_moderator',)
    search_fields = ('username', 'phone_number',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    list_filter = ()

    fieldsets = (
        (None, {
            "fields": (
                'username', 'password', 'first_name', 'last_name', 'phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_user', 'is_moderator', 'groups', 'user_permissions')}),
        ('Personal', {'fields': ('date_joined', 'last_login')})
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_superuser', 'is_staff', 'is_user', 'is_moderator')
            }
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('followers', 'follow')