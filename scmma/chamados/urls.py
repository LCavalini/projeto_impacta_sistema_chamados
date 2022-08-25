from django.urls import path

from .views.generico import AutenticarUsuario, DesautenticarUsuario, Index, RedefinirSenha
from .views.cliente import AdicionarChamado, IndexChamados, IndexCliente
from .views.admin import (AdicionarTerminal, EditarTerminal, IndexAdmin, IndexClientes, AdicionarCliente,
                          EditarCliente, IndexTerminal, ReativarCliente, ReativarTerminal, RemoverCliente,
                          RemoverTerminal, VerCliente, VerTerminal)

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
    path('admin/', IndexAdmin.as_view(), name='index_admin'),
    path('cliente/', IndexCliente.as_view(), name='index_cliente'),
    path('cliente/chamados', IndexChamados.as_view(), name='index_chamado'),
    path('cliente/chamados/adicionar', AdicionarChamado.as_view(), name='adicionar_chamado'),
    path('login/', AutenticarUsuario.as_view(), name='autenticar_usuario'),
    path('logout/', DesautenticarUsuario.as_view(), name='desautenticar_usuario'),
    path('redefinir/', RedefinirSenha.as_view(), name='redefinir_senha'),
    path('', Index.as_view(), name='index')
]
