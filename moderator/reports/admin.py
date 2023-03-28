from django.contrib import admin
from .models import Category, Report, ReportContent

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """"""


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """"""

@admin.register(ReportContent)
class ReportContentAdmin(admin.ModelAdmin):
    """"""
