from django import forms
from django.forms.models import BaseInlineFormSet
from posts.models import Post
from .models import (Point, PointFunction, TotalPoint)



class PointFunctionForm(forms.ModelForm):
    comment_on_post = forms.ModelChoiceField(queryset=Post.objects.all(), required=False,
                                           widget=forms.Select(attrs={'hidden': 'hidden'}))

    class Meta:
        model = PointFunction
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        when = cleaned_data.get('when')
        comment_on_post = cleaned_data.get('comment_on_post')

        if when == 3 and not comment_on_post:
            self.add_error('comment_on_post', 'Please chose post to validate')


class PointFunctionFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form