from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import AdicionarClienteForm, AdicionarTerminalForm
from ..models import Usuario, Terminal, Cliente


class AdicionarCliente(LoginRequiredMixin, CreateView):
    template_name = 'admin/clientes/adicionar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'

    def form_valid(self, form):
        usuario = form.save()
        cliente = Cliente()
        cliente.usuario = usuario
        cliente.save()
        return super(AdicionarCliente, self).form_valid(form)


class IndexClientes(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin/clientes/index.html'
    context_object_name = 'lista_clientes'
    login_url = 'autenticar_usuario'


class EditarCliente(LoginRequiredMixin, UpdateView):
    template_name = 'admin/clientes/editar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'


class VerCliente(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin/clientes/ver.html'
    context_object_name = 'cliente'
    login_url = 'autenticar_usuario'


class RemoverCliente(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin/clientes/remover.html'
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        return HttpResponseRedirect(self.get_success_url)


class AdicionarTerminal(LoginRequiredMixin, CreateView):
    template_name = 'admin/terminais/adicionar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'


class IndexTerminal(LoginRequiredMixin, ListView):
    model = Terminal
    template_name = 'admin/terminais/index.html'
    context_object_name = 'lista_terminais'
    login_url = 'autenticar_usuario'


class EditarTerminal(LoginRequiredMixin, UpdateView):
    template_name = 'admin/terminais/editar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'


class VerTerminal(LoginRequiredMixin, DetailView):
    model = Terminal
    template_name = 'admin/terminais/ver.html'
    context_object_name = 'terminal'
    login_url = 'autenticar_usuario'


class RemoverTerminal(LoginRequiredMixin, DeleteView):
    model = Terminal
    template_name = 'admin/terminais/remover.html'
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        return HttpResponseRedirect(self.get_success_url)


class IndexAdmin(LoginRequiredMixin, TemplateView):
    template_name = 'admin/index.html'
    login_url = 'autenticar_usuario'
