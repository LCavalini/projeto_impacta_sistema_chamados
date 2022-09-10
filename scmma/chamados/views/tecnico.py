from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.views.generic import ListView, TemplateView, View, DetailView
from django.urls import reverse_lazy

from ..exceptions import SemTecnicosDisponiveisException
from ..forms import EncerrarChamadoForm, TransferirChamadoForm
from ..models import Chamado, Usuario, Atendimento


class IndexChamados(PermissionRequiredMixin, ListView):
    model = Chamado
    template_name = 'tecnico/chamados/index.html'
    context_object_name = 'chamados'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    # Mostra apenas os chamados do usuário autenticado e que não foram transferidos
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(atendimento__tecnico=self.request.user,
                                                            atendimento__transferido=False)


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
        self.request.user.tecnico_ocupado = True  # o técnico fica ocupado por padrão ao atender um chamado
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
        chamado.estado = 3
        chamado.save()
        self.request.user.tecnico_ocupado = False  # o técnico fica não ocupado por padrão ao encerrar o chamado
        self.request.user.save()
        return HttpResponseRedirect(self.success_url)


class TransferirChamado(PermissionRequiredMixin, View):
    template_name = 'tecnico/chamados/transferir.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
    success_url = reverse_lazy('index_tecnico_chamado')
    form_class = TransferirChamadoForm

    def get(self, request, *args, **kwargs) -> HttpResponse:
        chamado = Chamado.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(nivel_tecnico=self.request.user.nivel)
        return render(request, template_name=self.template_name, context={'form': form, 'chamado': chamado})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        try:
            with transaction.atomic():
                tecnico = self.request.user
                tipo_transferencia = self.request.POST['tipo_transferencia']
                chamado = Chamado.objects.get(pk=self.kwargs['pk'])
                atendimento_encerrado = Atendimento.objects.filter(chamado=chamado, tecnico=self.request.user.pk).last()
                atendimento_encerrado.atividades = self.request.POST['atividades']
                atendimento_encerrado.transferido = True
                atendimento_encerrado.motivo_transferencia = self.request.POST['motivo_transferencia']
                atendimento_encerrado.save()
                novo_nivel = tecnico.nivel + 1 if tipo_transferencia == 'nivel_superior' else tecnico.nivel
                novo_atendimento = Atendimento.objects.create_atendimento(nivel=novo_nivel, ignorar_tecnicos=[tecnico],
                                                                          chamado=chamado)
                novo_atendimento.save()
                chamado.estado = 1  # chamado alocado
                chamado.save()
        except SemTecnicosDisponiveisException as e:
            messages.add_message(request, level=messages.ERROR, message=f'Erro ao transferir o chamado: {str(e)}')
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
        if 'HTTP_REFERER' in request.META:
            pagina_seguinte = request.META['HTTP_REFERER']
        else:
            pagina_seguinte = reverse_lazy('index_tecnico')
        return HttpResponseRedirect(pagina_seguinte)


class AtualizarDisponibilidade(PermissionRequiredMixin, View):
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        tecnico_ocupado = False if request.POST['tecnico_ocupado'] == 'false' else True
        tecnico = Usuario.objects.get(pk=request.user.pk)
        tecnico.tecnico_ocupado = tecnico_ocupado
        tecnico.save()
        if 'HTTP_REFERER' in request.META:
            pagina_seguinte = request.META['HTTP_REFERER']
        else:
            pagina_seguinte = reverse_lazy('index_tecnico')
        return HttpResponseRedirect(pagina_seguinte)


class IndexTecnico(PermissionRequiredMixin, TemplateView):
    template_name = 'tecnico/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
