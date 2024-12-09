from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def login_exists(value):
    if User.objects.filter(login=value):
        raise ValidationError(
            _("Данный логин уже существует!"),
            params={"value": value},
        )
