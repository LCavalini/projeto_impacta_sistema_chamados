from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login
from django.shortcuts import HttpResponseRedirect

from ..forms import AutenticarUsuarioForm


class AutenticarUsuario(LoginView):
    template_name = 'login.html'
    form_class = AutenticarUsuarioForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.user.is_superuser:
            self.next_page = 'index_admin'
        elif self.request.user.user_type == 0:
            self.next_page = 'index_cliente'
        return HttpResponseRedirect(self.get_success_url())


class DesautenticarUsuario(LogoutView):
    next_page = 'autenticar_usuario'
