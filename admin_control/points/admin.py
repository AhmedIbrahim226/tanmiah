from django import forms
from django.contrib import admin
from .models import (Point, PointFunction, TotalPointFunction)
from django.forms.models import BaseInlineFormSet

""
class PointFunctionFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
    
    def clean(self):
        ctx = super().clean()
        for f in self.forms:
            print(f.cleaned_data)
        return ctx


class InlinePointFunction(admin.TabularInline):
    class Media:
        js = ("admin/js/custom.js",)

    model = PointFunction
    extra = 1
    formset = PointFunctionFormSet


@admin.register(PointFunction)
class PointFunctionAdmin(admin.ModelAdmin):
    """"""
""

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    """"""
    inlines = [InlinePointFunction]




@admin.register(TotalPointFunction)
class TotalPointFunctionAdmin(admin.ModelAdmin):
    """"""