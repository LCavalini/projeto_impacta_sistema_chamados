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

    def __init__(self, request=None, *args, **kwargs):
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
                'Usuário inativo. Entre em contato com o Administrador.',
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            'Email ou senha incorretos',
            code="invalid_login"
        )
