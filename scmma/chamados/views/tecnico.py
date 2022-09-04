from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, TemplateView, View
from django.shortcuts import HttpResponseRedirect

from ..models import Chamado, Usuario


class IndexChamados(PermissionRequiredMixin, ListView):
    model = Chamado
    template_name = 'tecnico/chamados/index.html'
    context_object_name = 'chamados'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'

    # Mostra apenas os chamados do usuário autenticado
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(atendimento__tecnico=self.request.user)


class AtualizarLocalizacao(View):

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        tecnico = Usuario.objects.get(pk=request.user.pk)
        tecnico.ultima_latitude = latitude
        tecnico.ultima_longitude = longitude
        tecnico.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class IndexTecnico(PermissionRequiredMixin, TemplateView):
    template_name = 'tecnico/index.html'
    login_url = 'autenticar_usuario'
    permission_required = 'chamados.change_chamado'
