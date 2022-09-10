from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView, DetailView, TemplateView

from ..exceptions import ConfiguracaoGeolocalizacaoException
from ..forms import (AdicionarClienteForm, AdicionarTecnicoForm, AdicionarTerminalForm, ReativarClienteForm,
                     ReativarTerminalForm, ReativarTecnicoForm)
from ..models import Usuario, Terminal


class AdicionarCliente(PermissionRequiredMixin, CreateView):
    template_name = 'admin/clientes/adicionar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_usuario'

    def form_valid(self, form) -> HttpResponse:
        usuario = form.save()
        usuario.tipo_usuario = 0  # tipo de usuário é Cliente
        usuario.set_password(Usuario.objects.make_random_password())  # gera uma senha aleatória inicial
        permissoes = [
            Permission.objects.get(codename='add_chamado'),
            Permission.objects.get(codename='view_chamado')
        ]
        usuario.user_permissions.set(permissoes)
        return super().form_valid(form)


class IndexClientes(PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin/clientes/index.html'
    context_object_name = 'clientes'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_usuario'


class EditarCliente(PermissionRequiredMixin, UpdateView):
    template_name = 'admin/clientes/editar.html'
    model = Usuario
    form_class = AdicionarClienteForm
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_usuario'


class VerCliente(PermissionRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin/clientes/ver.html'
    context_object_name = 'usuario'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_usuario'


class RemoverCliente(PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin/clientes/remover.html'
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.delete_usuario'

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Exclui os usuários de forma não definitiva (apenas altera o atributo is_active).
        """
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        return self.delete(request, *args, **kwargs)


class ReativarCliente(PermissionRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'admin/clientes/reativar.html'
    success_url = reverse_lazy('admin_index_cliente')
    login_url = 'autenticar_usuario'
    form_class = ReativarClienteForm
    permission_required = 'chamados.delete_usuario'

    def form_valid(self, form) -> HttpResponse:
        self.object.is_active = True
        return super().form_valid(form)


class AdicionarTerminal(PermissionRequiredMixin, CreateView):
    template_name = 'admin/terminais/adicionar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_terminal'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ConfiguracaoGeolocalizacaoException as e:
            messages.add_message(request, messages.ERROR, str(e))
            return render(request, self.template_name, context={'form': self.get_form()})


class IndexTerminal(PermissionRequiredMixin, ListView):
    model = Terminal
    template_name = 'admin/terminais/index.html'
    context_object_name = 'terminais'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_terminal'


class EditarTerminal(PermissionRequiredMixin, UpdateView):
    template_name = 'admin/terminais/editar.html'
    model = Terminal
    form_class = AdicionarTerminalForm
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_terminal'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ConfiguracaoGeolocalizacaoException as e:
            messages.add_message(request, messages.ERROR, str(e))
            return render(request, self.template_name, context={'form': self.get_form()})


class VerTerminal(PermissionRequiredMixin, DetailView):
    model = Terminal
    template_name = 'admin/terminais/ver.html'
    context_object_name = 'terminal'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_terminal'


class RemoverTerminal(PermissionRequiredMixin, DeleteView):
    model = Terminal
    template_name = 'admin/terminais/remover.html'
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.delete_terminal'

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Exclui os terminais de forma não definitiva (apenas altera o atributo is_active).
        """
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        return self.delete(request, *args, **kwargs)


class ReativarTerminal(PermissionRequiredMixin, UpdateView):
    model = Terminal
    template_name = 'admin/terminais/reativar.html'
    success_url = reverse_lazy('admin_index_terminal')
    login_url = 'autenticar_usuario'
    form_class = ReativarTerminalForm
    permission_required = 'chamados.delete_terminal'

    def form_valid(self, form) -> HttpResponse:
        self.object.is_active = True
        return super().form_valid(form)


class AdicionarTecnico(PermissionRequiredMixin, CreateView):
    template_name = 'admin/tecnicos/adicionar.html'
    model = Usuario
    form_class = AdicionarTecnicoForm
    success_url = reverse_lazy('admin_index_tecnico')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_usuario'

    def form_valid(self, form) -> HttpResponse:
        usuario = form.save()
        usuario.tipo_usuario = 1  # tipo de usuário é Técnico
        usuario.set_password(Usuario.objects.make_random_password())  # gera uma senha aleatória inicial
        permissoes = [
            Permission.objects.get(codename='view_chamado'),
            Permission.objects.get(codename='change_chamado')
        ]
        usuario.user_permissions.set(permissoes)
        return super().form_valid(form)


class IndexTecnicos(PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin/tecnicos/index.html'
    context_object_name = 'tecnicos'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_usuario'


class EditarTecnico(PermissionRequiredMixin, UpdateView):
    template_name = 'admin/tecnicos/editar.html'
    model = Usuario
    form_class = AdicionarTecnicoForm
    success_url = reverse_lazy('admin_index_tecnico')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_usuario'


class VerTecnico(PermissionRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin/tecnicos/ver.html'
    context_object_name = 'usuario'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.view_usuario'


class RemoverTecnico(PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin/tecnicos/remover.html'
    success_url = reverse_lazy('admin_index_tecnico')
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.delete_usuario'

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Exclui os usuários de forma não definitiva (apenas altera o atributo is_active).
        """
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        return self.delete(request, *args, **kwargs)


class ReativarTecnico(PermissionRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'admin/tecnicos/reativar.html'
    success_url = reverse_lazy('admin_index_tecnico')
    login_url = 'autenticar_usuario'
    form_class = ReativarTecnicoForm
    permission_required = 'chamados.delete_usuario'

    def form_valid(self, form) -> HttpResponse:
        self.object.is_active = True
        return super().form_valid(form)


class IndexAdmin(PermissionRequiredMixin, TemplateView):
    template_name = 'admin/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.add_usuario'
