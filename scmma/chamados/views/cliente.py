from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import HttpResponse, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView

from ..forms import AdicionarChamadoForm
from ..models import Chamado


class AdicionarChamado(PermissionRequiredMixin, CreateView):
    model = Chamado
    form_class = AdicionarChamadoForm
    template_name = 'cliente/chamados/adicionar.html'
    success_url = reverse_lazy('index_cliente_chamado')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_chamado'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            # o usuário que abre o chamado é o usuário autenticado
            form = self.form_class(usuario=request.user)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def get_form_kwargs(self) -> dict:
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        # o usuário que abre o chamado é o usuário autenticado
        if self.request.user.is_authenticated:
            kwargs['usuario'] = self.request.user
        return kwargs


class IndexChamados(PermissionRequiredMixin, ListView):
    model = Chamado
    template_name = 'cliente/chamados/index.html'
    context_object_name = 'chamados'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_chamado'

    # Mostra apenas os chamados do usuário autenticado
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(usuario=self.request.user)


class IndexCliente(PermissionRequiredMixin, TemplateView):
    template_name = 'cliente/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_chamado'
