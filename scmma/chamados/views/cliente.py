from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


from ..models import Chamado
from ..forms import AdicionarChamadoForm


class AdicionarChamado(PermissionRequiredMixin, CreateView):
    model = Chamado
    form_class = AdicionarChamadoForm
    template_name = 'cliente/chamados/adicionar.html'
    success_url = reverse_lazy('index_chamado')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_chamado'


class IndexChamados(PermissionRequiredMixin, ListView):
    model = Chamado
    template_name = 'cliente/chamados/index.html'
    context_object_name = 'lista_chamados'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_chamado'


class IndexCliente(PermissionRequiredMixin, TemplateView):
    template_name = 'cliente/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_chamado'
