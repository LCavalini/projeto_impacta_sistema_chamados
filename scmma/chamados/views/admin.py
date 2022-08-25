from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission

from ..forms import AdicionarClienteForm, AdicionarTerminalForm, ReativarClienteForm, ReativarTerminalForm
from ..models import Usuario, Terminal


class AdicionarCliente(PermissionRequiredMixin, CreateView):
    template_name = 'admin/clientes/adicionar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'add_usuario'

    def form_valid(self, form):
        usuario = form.save()
        usuario.tipo_usuario = 0  # tipo de usuário é Cliente
        permissoes = [
            Permission.objects.get(codename='add_chamado'),
            Permission.objects.get(codename='view_chamado')
        ]
        usuario.user_permissions.set(permissoes)
        return super().form_valid(form)


class IndexClientes(PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin/clientes/index.html'
    context_object_name = 'lista_clientes'
    login_url = 'autenticar_usuario'
    permission_required = 'view_usuario'


class EditarCliente(PermissionRequiredMixin, UpdateView):
    template_name = 'admin/clientes/editar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'change_usuario'


class VerCliente(PermissionRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin/clientes/ver.html'
    context_object_name = 'cliente'
    login_url = 'autenticar_usuario'
    permission_required = 'view_usuario'


class RemoverCliente(PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin/clientes/remover.html'
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'delete_usuario'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ReativarCliente(PermissionRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'admin/clientes/reativar.html'
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    form_class = ReativarClienteForm
    permission_required = 'delete_usuario'

    def form_valid(self, form):
        self.object.is_active = True
        return super().form_valid(form)


class AdicionarTerminal(PermissionRequiredMixin, CreateView):
    template_name = 'admin/terminais/adicionar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'add_terminal'


class IndexTerminal(PermissionRequiredMixin, ListView):
    model = Terminal
    template_name = 'admin/terminais/index.html'
    context_object_name = 'lista_terminais'
    login_url = 'autenticar_usuario'
    permission_required = 'view_terminal'


class EditarTerminal(PermissionRequiredMixin, UpdateView):
    template_name = 'admin/terminais/editar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'change_terminal'


class VerTerminal(PermissionRequiredMixin, DetailView):
    model = Terminal
    template_name = 'admin/terminais/ver.html'
    context_object_name = 'terminal'
    login_url = 'autenticar_usuario'
    permission_required = 'view_terminal'


class RemoverTerminal(PermissionRequiredMixin, DeleteView):
    model = Terminal
    template_name = 'admin/terminais/remover.html'
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'delete_terminal'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ReativarTerminal(PermissionRequiredMixin, UpdateView):
    model = Terminal
    template_name = 'admin/terminais/reativar.html'
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    form_class = ReativarTerminalForm
    permission_required = 'delete_terminal'

    def form_valid(self, form):
        self.object.is_active = True
        return super().form_valid(form)


class IndexAdmin(PermissionRequiredMixin, TemplateView):
    template_name = 'admin/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'add_usuario'
