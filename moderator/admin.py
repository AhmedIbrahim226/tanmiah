from django.contrib import admin
from django.db.models import F

from posts.models import PostMedia
from .models import PostProxy
from .points.models import PointFunction, UserPointFunctionEarning, TotalPoint
import logging

class PostMediaInline(admin.TabularInline):
    model = PostMedia

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


logger = logging.getLogger('points')
def manage_point_functions_on_post(obj, functions):
    if functions.exists():
        for func in functions:
            check_to_increase, created = UserPointFunctionEarning.objects.get_or_create(
                owner=obj.owner,
                point_function=func,
                defaults={'earns_until_now': func.earn}
            )
            if func.deduction:
                if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
                    TotalPoint.objects.filter(point=func.point, user=obj.owner).update(
                        total_earning=F('total_earning') - func.earn)
                    logger.warning(f'{func.earn} points are deducted from the user from point: {func.point.singular_name} ==> {func.get_when_str}', extra={'username': obj.owner.username})
                    if not created:
                        check_to_increase.earns_until_now += func.earn
                        check_to_increase.save()
            else:
                if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
                    TotalPoint.objects.filter(point=func.point, user=obj.owner).update(
                        total_earning=F('total_earning') + func.earn)
                    logger.info(f'{func.earn} points earned by the user from point: {func.point.singular_name} ==> {func.get_when_str}', extra={'username': obj.owner.username})
                    if not created:
                        check_to_increase.earns_until_now += func.earn
                        check_to_increase.save()


@admin.register(PostProxy)
class PostProxyAdmin(admin.ModelAdmin):
    filter_horizontal = ('share_with',)
    def has_add_permission(self, request):
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
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        if obj.point_game:
            """without media option media = 4"""
            if obj.media == 4:
                functions = PointFunction.objects.select_related('point').filter(when=1, active=True)
                manage_point_functions_on_post(obj, functions)
                return super().save_model(request, obj, form, change)
            else:
                """with media option media = [1 | 2 | 3]"""
                functions = PointFunction.objects.select_related('point').filter(when=2, active=True)
                manage_point_functions_on_post(obj, functions)
                return super().save_model(request, obj, form, change)
        return super().save_model(request, obj, form, change)