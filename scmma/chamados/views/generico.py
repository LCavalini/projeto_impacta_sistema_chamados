from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy

from ..forms import AutenticarUsuarioForm, RedefinirSenhaForm


class AutenticarUsuario(LoginView):
    template_name = 'login.html'
    form_class = AutenticarUsuarioForm
    redirect_authenticated_user = True
    next_page = 'index'


class DesautenticarUsuario(LogoutView):
    next_page = 'autenticar_usuario'


class RedefinirSenha(PasswordResetView):
    template_name = 'redefinir_senha/index.html'
    email_template_name = 'redefinir_senha/texto_email.html'
    subject_template_name = 'redefinir_senha/assunto_email.txt'
    success_url = reverse_lazy('redefinir_senha_enviado')
    form_class = RedefinirSenhaForm


class RedefinirSenhaEnviado(TemplateView):
    template_name = 'redefinir_senha/sucesso.html'


class RedefinirSenhaConfirmar(PasswordResetConfirmView):
    template_name = 'redefinir_senha/confirmar.html'
    success_url = reverse_lazy('redefinir_senha_completo')


class RedefinirSenhaCompleta(PasswordResetCompleteView):
    template_name = 'redefinir_senha/completo.html'


class Index(LoginRequiredMixin, View):
    login_url = 'autenticar_usuario'

    def get(self, request):
        if request.user.tipo_usuario == 'Cliente':
            return HttpResponseRedirect(reverse_lazy('index_cliente'))
        elif request.user.tipo_usuario == 'Administrador':
            return HttpResponseRedirect(reverse_lazy('index_admin'))
