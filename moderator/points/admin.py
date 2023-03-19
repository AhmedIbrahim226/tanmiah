from django.contrib import admin
from django.utils.html import html_safe

from .forms import PointFunctionForm, PointFunctionFormSet
from .models import (Point, PointFunction, UserPointFunctionEarning, TotalPoint, PointLog)


@html_safe
class JSPath:
    def __str__(self):
        return '<script defer src="/static/admin/js/inline_point_function.js/"></script>'


class InlinePointFunction(admin.TabularInline):
    model = PointFunction
    extra = 1
    form = PointFunctionForm
    formset = PointFunctionFormSet

    class Media:
        js = (JSPath(),)


@admin.register(PointFunction)
class PointFunctionAdmin(admin.ModelAdmin):
    """"""


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    """"""
    inlines = [InlinePointFunction]


@admin.register(TotalPoint)
class TotalPointAdmin(admin.ModelAdmin):
    """"""


@admin.register(UserPointFunctionEarning)
class UserPointFunctionEarningAdmin(admin.ModelAdmin):
    """"""


@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):
    list_display = ('point', 'log', 'view_created_at')
    search_fields = ('point__singular_name', 'log', 'created_at')
    readonly_fields = ('view_created_at',)
    list_display_links = None

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    @admin.display(empty_value='???')
    def view_created_at(self, obj):
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")
