from django.contrib import admin
from .models import (Point, PointFunction, UserPointFunctionEarning, TotalPoint)
from django.utils.html import html_safe
from .forms import PointFunctionForm, PointFunctionFormSet


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