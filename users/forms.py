from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import UserAuth, UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import authenticate



class UserRegisterForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='EG'))
    class Meta:
        model = UserAuth
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'phone_number',)

    """ 
    def clean_is_moderator(self):
        # User must specify one role.

        is_user = self.cleaned_data.get('is_user')
        is_moderator = self.cleaned_data.get('is_moderator')
        if is_user and is_moderator:
            raise ValidationError('User must specify one role.')
        
        return is_moderator
    """



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), required=False)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='EG'), required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
    

    def clean(self):
        username = self.cleaned_data.get("username")
        phone_number = self.cleaned_data.get("phone_number")
        password = self.cleaned_data.get("password")

        username = phone_number or username

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'followers', 'follow',)
