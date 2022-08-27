from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse_lazy

from chamados.models import Usuario, Terminal, Chamado


class TestCadastramentoChamados(TestCase):

    def setUp(self) -> None:
        self.cliente_web = Client()
        self.usuario_cliente = Usuario(email='cliente@cliente.com', password='123', tipo_usuario=0)
        self.usuario_cliente.save()
        permissoes = [
            Permission.objects.get(codename='add_chamado'),
            Permission.objects.get(codename='view_chamado')
        ]
        self.usuario_cliente.user_permissions.set(permissoes)
        self.usuario_cliente.save()
        self.cliente_web.force_login(self.usuario_cliente)
        self.terminal = Terminal(numero_serie='123', usuario=self.usuario_cliente)
        self.terminal.save()

    def test_abrir_chamado(self) -> None:
        dados = {
            'tipo': 'erro_leitura_cartao',
            'descricao': 'A máquina não está conseguindo ler os cartões dos usuários',
            'gravidade': 1,
            'usuario': self.usuario_cliente.pk,
            'terminal': self.terminal.pk
        }
        caminho = reverse_lazy('adicionar_chamado')
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('index_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        chamado = Chamado.objects.get(tipo=dados['tipo'])
        resultado = chamado.descricao
        esperado = dados['descricao']
        self.assertEqual(resultado, esperado)  # teste de banco de dados
