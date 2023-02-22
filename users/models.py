from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.humanize.templatetags.humanize import naturalday

class UserAuthManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, phone_number, password=None):

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, phone_number, password):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)
        return user


class UserAuth(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone_number = PhoneNumberField(region="EG", unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_user = models.BooleanField(_('user status'), default=False, help_text=_('Designates if the user has a non-privileged user.'))
    is_moderator = models.BooleanField(_('moderator status'), default=False, help_text=_('Designates whether the user permissions as moderator.'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserAuthManager()

    def __str__(self):
        return self.username

    @cached_property
    def ret_naturalday_joined(self):
        return naturalday(self.date_joined)



class UserProfile(models.Model):
    owner = models.OneToOneField(UserAuth, on_delete=models.CASCADE, related_name='profile')
    bg_img = models.ImageField(upload_to='users/profiles/bg/', blank=True, null=True)
    personal_img = models.ImageField(upload_to='users/profiles/ps/', blank=True, null=True)
    followers = models.ManyToManyField(UserAuth, related_name='followers', blank=True)
    follow = models.ManyToManyField(UserAuth, related_name='follow', blank=True)
    active_now = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username


