from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from .models import Chamado, Terminal, Usuario

UserModel = get_user_model()


class AdicionarClienteForm(ModelForm):

    class Meta:
        model = Usuario
        fields = Usuario.CAMPOS_CLIENTE


class ReativarClienteForm(ModelForm):

    class Meta:
        model = Usuario
        fields = []


class AdicionarTerminalForm(ModelForm):

    class Meta:
        model = Terminal
        fields = ['data_instalacao', 'numero_serie', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
                  'cep', 'usuario']


class ReativarTerminalForm(ModelForm):

    class Meta:
        model = Terminal
        fields = []


class AdicionarChamadoForm(ModelForm):

    class Meta:
        model = Chamado
        fields = ['tipo', 'descricao', 'gravidade', 'usuario', 'terminal']


class RedefinirSenhaForm(PasswordResetForm):
    pass


class AutenticarUsuarioForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email.verbose_name},
        )
