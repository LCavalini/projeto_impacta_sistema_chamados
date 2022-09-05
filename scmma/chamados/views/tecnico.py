from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.views.generic import ListView, TemplateView, View, DetailView
from django.urls import reverse_lazy

from ..forms import EncerrarChamadoForm
from ..models import Chamado, Usuario, Atendimento


class IndexChamados(PermissionRequiredMixin, ListView):
    model = Chamado
    template_name = 'tecnico/chamados/index.html'
    context_object_name = 'chamados'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    # Mostra apenas os chamados do usuário autenticado
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(atendimento__tecnico=self.request.user)


class VerChamado(PermissionRequiredMixin, DetailView):
    model = Chamado
    template_name = 'tecnico/chamados/ver.html'
    context_object_name = 'chamado'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'


class HistoricoChamado(PermissionRequiredMixin, DetailView):
    model = Atendimento
    template_name = 'tecnico/chamados/historico.html'
    context_object_name = 'atendimentos'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    # Mostra todos os atendimentos do chamado
    def get_object(self, *args, **kwargs):
        chamado = self.kwargs['pk']
        return Atendimento.objects.filter(chamado=chamado)


class AtenderChamado(PermissionRequiredMixin, DetailView):
    model = Chamado
    template_name = 'tecnico/chamados/atender.html'
    context_object_name = 'chamado'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
    success_url = reverse_lazy('index_tecnico_chamado')

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        chamado = Chamado.objects.get(pk=self.kwargs['pk'])
        chamado.estado = 2
        chamado.save()
        self.request.user.tecnico_ocupado = True
        self.request.user.save()
        return HttpResponseRedirect(self.success_url)


class EncerrarChamado(PermissionRequiredMixin, View):
    template_name = 'tecnico/chamados/encerrar.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
    success_url = reverse_lazy('index_tecnico_chamado')
    form_class = EncerrarChamadoForm

    def get(self, request, *args, **kwargs) -> HttpResponse:
        chamado = Chamado.objects.get(pk=self.kwargs['pk'])
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form, 'chamado': chamado})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        chamado = Chamado.objects.get(pk=self.kwargs['pk'])
        atendimento = Atendimento.objects.filter(chamado=chamado, tecnico=self.request.user.pk).last()
        atendimento.atividades = self.request.POST['atividades']
        atendimento.save()
        chamado.estado = 4
        chamado.save()
        return HttpResponseRedirect(self.success_url)


class AtualizarLocalizacao(PermissionRequiredMixin, View):
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        tecnico = Usuario.objects.get(pk=request.user.pk)
        tecnico.ultima_latitude = latitude
        tecnico.ultima_longitude = longitude
        tecnico.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class AtualizarDisponibilidade(PermissionRequiredMixin, View):
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        tecnico_ocupado = False if request.POST['tecnico_ocupado'] == 'false' else True
        tecnico = Usuario.objects.get(pk=request.user.pk)
        tecnico.tecnico_ocupado = tecnico_ocupado
        tecnico.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexTecnico(PermissionRequiredMixin, TemplateView):
    template_name = 'tecnico/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
