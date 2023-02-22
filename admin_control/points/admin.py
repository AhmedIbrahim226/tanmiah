from django import forms
from django.contrib import admin
from .models import (Point, PointFunction, TotalPointFunction)


""
class PointFunctionForm(forms.ModelForm):
    class Meta:
        model = PointFunction
        fields = "__all__"


PointFunctionFormSet = forms.formset_factory(PointFunctionForm, max_num=1)


class InlinePointFunction(admin.TabularInline):
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