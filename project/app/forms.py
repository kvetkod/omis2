from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=254)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class Do_DZ(forms.Form):
    do_dz = forms.CharField(label="Ответ")


class DoTest(forms.Form):
    do_test = forms.CharField(label="Ответ")


class Search(forms.Form):
    search = forms.CharField(label="Поиск:")
