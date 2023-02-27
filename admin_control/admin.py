from django.contrib import admin

from posts.models import PostMedia
from .models import PostProxy


class PostMediaInline(admin.TabularInline):
    model = PostMedia

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(PostProxy)
class PostProxyAdmin(admin.ModelAdmin):
    filter_horizontal = ('share_with',)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def get_inlines(self, request, obj):
        if obj.media != 4:
            return [PostMediaInline]
        return super().get_inlines(request, obj)

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if field.name != 'safe'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        safe = form.cleaned_data.get('safe')
        if change and not safe:
            return obj.delete()
        return super().save_model(request, obj, form, change)