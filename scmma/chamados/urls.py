from django.urls import path

from .views.generico import (AutenticarUsuario, DesautenticarUsuario, Index, RedefinirSenha, RedefinirSenhaCompleta,
                             RedefinirSenhaConfirmar, RedefinirSenhaEnviado)
from .views.cliente import AdicionarChamado, IndexChamados as IndexClienteChamados, IndexCliente
from .views.tecnico import (AtenderChamado, AtualizarDisponibilidade, EncerrarChamado, HistoricoChamado,
                            IndexChamados as IndexTecnicoChamados, IndexTecnico, AtualizarLocalizacao, VerChamado)
from .views.admin import (AdicionarTecnico, AdicionarTerminal, EditarTerminal, IndexAdmin, IndexClientes,
                          AdicionarCliente, EditarCliente, IndexTecnicos, IndexTerminal, ReativarCliente,
                          ReativarTecnico, ReativarTerminal, RemoverCliente, RemoverTecnico, EditarTecnico,
                          VerTecnico, RemoverTerminal, VerCliente, VerTerminal)

urlpatterns = [
    path('admin/clientes', IndexClientes.as_view(), name='admin_index_cliente'),
    path('admin/clientes/adicionar', AdicionarCliente.as_view(), name='adicionar_cliente'),
    path('admin/clientes/editar/<int:pk>', EditarCliente.as_view(), name='editar_cliente'),
    path('admin/clientes/ver/<int:pk>', VerCliente.as_view(), name='ver_cliente'),
    path('admin/clientes/remover/<int:pk>', RemoverCliente.as_view(), name='remover_cliente'),
    path('admin/clientes/reativar/<int:pk>', ReativarCliente.as_view(), name='reativar_cliente'),
    path('admin/terminais', IndexTerminal.as_view(), name='admin_index_terminal'),
    path('admin/terminais/adicionar', AdicionarTerminal.as_view(), name='adicionar_terminal'),
    path('admin/terminais/editar/<int:pk>', EditarTerminal.as_view(), name='editar_terminal'),
    path('admin/terminais/ver/<int:pk>', VerTerminal.as_view(), name='ver_terminal'),
    path('admin/terminais/remover/<int:pk>', RemoverTerminal.as_view(), name='remover_terminal'),
    path('admin/terminais/reativar/<int:pk>', ReativarTerminal.as_view(), name='reativar_terminal'),
    path('admin/tecnicos', IndexTecnicos.as_view(), name='admin_index_tecnico'),
    path('admin/tecnicos/adicionar', AdicionarTecnico.as_view(), name='adicionar_tecnico'),
    path('admin/tecnicos/editar/<int:pk>', EditarTecnico.as_view(), name='editar_tecnico'),
    path('admin/tecnicos/ver/<int:pk>', VerTecnico.as_view(), name='ver_tecnico'),
    path('admin/tecnicos/remover/<int:pk>', RemoverTecnico.as_view(), name='remover_tecnico'),
    path('admin/tecnicos/reativar/<int:pk>', ReativarTecnico.as_view(), name='reativar_tecnico'),
    path('admin/', IndexAdmin.as_view(), name='index_admin'),
    path('cliente/', IndexCliente.as_view(), name='index_cliente'),
    path('cliente/chamados', IndexClienteChamados.as_view(), name='index_cliente_chamado'),
    path('cliente/chamados/adicionar', AdicionarChamado.as_view(), name='adicionar_chamado'),
    path('tecnico/', IndexTecnico.as_view(), name='index_tecnico'),
    path('tecnico/chamados', IndexTecnicoChamados.as_view(), name='index_tecnico_chamado'),
    path('tecnico/chamados/ver/<int:pk>', VerChamado.as_view(), name='ver_chamado'),
    path('tecnico/chamados/historico/<int:pk>', HistoricoChamado.as_view(), name='historico_chamado'),
    path('tecnico/chamados/atender/<int:pk>', AtenderChamado.as_view(), name='atender_chamado'),
    path('tecnico/chamados/encerrar/<int:pk>', EncerrarChamado.as_view(), name='encerrar_chamado'),
    path('tecnico/localizacao/atualizar', AtualizarLocalizacao.as_view(), name='atualizar_localizacao'),
    path('tecnico/disponibilidade/atualizar', AtualizarDisponibilidade.as_view(), name='atualizar_disponibilidade'),
    path('login/', AutenticarUsuario.as_view(), name='autenticar_usuario'),
    path('logout/', DesautenticarUsuario.as_view(), name='desautenticar_usuario'),
    path('redefinir/', RedefinirSenha.as_view(), name='redefinir_senha'),
    path('redefinir/enviado', RedefinirSenhaEnviado.as_view(), name='redefinir_senha_enviado'),
    path('redefinir/confirmar/<uidb64>/<token>/', RedefinirSenhaConfirmar.as_view(), name='redefinir_senha_confirmar'),
    path('redefinir/completo', RedefinirSenhaCompleta.as_view(), name='redefinir_senha_completo'),
    path('', Index.as_view(), name='index')
]
