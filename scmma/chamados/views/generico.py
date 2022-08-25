from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
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
    template_name = 'redefinir_senha.html'
    email_template_name = 'email_redefinir_senha.html'
    form_class = RedefinirSenhaForm


class Index(LoginRequiredMixin, View):
    login_url = 'autenticar_usuario'

    def get(self, request):
        if request.user.tipo_usuario == 'Cliente':
            return HttpResponseRedirect(reverse_lazy('index_cliente'))
        elif request.user.tipo_usuario == 'Administrador':
            return HttpResponseRedirect(reverse_lazy('index_admin'))
