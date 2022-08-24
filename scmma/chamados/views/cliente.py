from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from ..models import Chamado
from ..forms import AdicionarChamadoForm


class AdicionarChamado(LoginRequiredMixin, CreateView):
    model = Chamado
    form_class = AdicionarChamadoForm
    template_name = 'cliente/chamados/adicionar.html'
    success_url = reverse_lazy('index_chamado')
    login_url = 'autenticar_usuario'


class IndexChamados(LoginRequiredMixin, ListView):
    model = Chamado
    template_name = 'cliente/chamados/index.html'
    context_object_name = 'lista_chamados'
    login_url = 'autenticar_usuario'


class IndexCliente(LoginRequiredMixin, TemplateView):
    template_name = 'cliente/index.html'
    login_url = 'autenticar_usuario'
