from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Chamado, Terminal, Usuario

UserModel = get_user_model()


class AdicionarClienteForm(ModelForm):

    required_css_class = 'campo_obrigatorio'

    class Meta:
        model = Usuario
        fields = Usuario.CAMPOS_CLIENTE


class ReativarClienteForm(ModelForm):

    class Meta:
        model = Usuario
        fields = []


class AdicionarTecnicoForm(ModelForm):

    required_css_class = 'campo_obrigatorio'

    class Meta:
        model = Usuario
        fields = Usuario.CAMPOS_TECNICO


class ReativarTecnicoForm(ModelForm):

    class Meta:
        model = Usuario
        fields = []


class AdicionarTerminalForm(ModelForm):

    required_css_class = 'campo_obrigatorio'

    class Meta:
        model = Terminal
        fields = ['numero_serie', 'data_instalacao', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
                  'cep', 'usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # permite somente a seleção de clientes
        self.fields['usuario'].queryset = Usuario.objects.filter(_tipo_usuario=0)


class ReativarTerminalForm(ModelForm):

    class Meta:
        model = Terminal
        fields = []


class AdicionarChamadoForm(ModelForm):

    required_css_class = 'campo_obrigatorio'

    class Meta:
        model = Chamado
        fields = ['tipo', 'descricao', 'gravidade', 'terminal']

    def __init__(self, *args, **kwargs) -> None:
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        # limita as opções de terminais àqueles que são relacionados ao usuário autenticado
        if self.usuario is not None:
            self.fields['terminal'].queryset = Terminal.objects.filter(usuario=self.usuario.pk)
        else:
            self.fields['terminal'].queryset = Terminal.objects.none()

    def save(self, commit: bool = True):
        # atribui o chamado ao usuário autenticado
        self.instance.usuario = self.usuario
        return super().save(commit)


class RedefinirSenhaForm(PasswordResetForm):
    pass


class AutenticarUsuarioForm(forms.Form):
    """
    Autenticação de usuário baseado em email (em vez de username) e senha.
    """
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, request=None, *args, **kwargs) -> None:
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self) -> dict:
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

    def confirm_login_allowed(self, user) -> None:
        if not user.is_active:
            raise ValidationError(
                'Usuário inativo. Entre em contato com o Administrador.',
                code="inactive",
            )

    def get_user(self) -> AbstractUser:
        return self.user_cache

    def get_invalid_login_error(self) -> ValidationError:
        return ValidationError(
            'Email ou senha incorretos',
            code="invalid_login"
        )
