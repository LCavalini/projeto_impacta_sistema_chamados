from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse_lazy

from chamados.models import Usuario, Terminal, Chamado, Atendimento


class TestAlteracaoChamados(TestCase):

    def setUp(self) -> None:
        self.cliente_web = Client()
        self.cliente = Usuario(email='cliente@cliente.com', password='123', tipo_usuario=0)
        self.cliente.save()
        self.tecnico1 = Usuario(email='tecnico1@tecnico.com', tipo_usuario=1, ultima_latitude='-23.550389799999998',
                                ultima_longitude='-46.633080956332904', nivel=0)
        permissoes = [
            Permission.objects.get(codename='view_chamado'),
            Permission.objects.get(codename='change_chamado')
        ]
        self.tecnico1.save()
        self.tecnico1.user_permissions.set(permissoes)
        self.tecnico1.save()
        self.tecnico2 = Usuario(email='tecnico2@tecnico.com', tipo_usuario=1, ultima_latitude='-23.5610625',
                                ultima_longitude='-46.6612816', nivel=0)
        self.tecnico2.save()
        self.tecnico3 = Usuario(email='tecnico3@tecnico.com', tipo_usuario=1, ultima_latitude='-23.5255246',
                                ultima_longitude='-46.6517839', nivel=1)
        self.tecnico3.save()
        self.cliente_web.force_login(self.tecnico1)
        self.terminal = Terminal(numero_serie='123', usuario=self.cliente, rua='Praça da Sé', bairro='Sé',
                                 cidade='São Paulo', estado='SP')
        self.terminal.save()
        self.chamado = Chamado.objects.create_chamado(
            tipo='erro_leitura_cartao',
            descricao='A máquina não está conseguindo ler os cartões dos usuários',
            gravidade=1,
            usuario=self.cliente,
            terminal=self.terminal
        )

    def test_atender_chamado(self):
        caminho = reverse_lazy('atender_chamado', kwargs={'pk': self.chamado.pk})
        resposta = self.cliente_web.post(caminho)
        resultado = resposta
        esperado = reverse_lazy('index_tecnico_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        chamado = Chamado.objects.get(pk=self.chamado.pk)
        resultado = chamado.estado
        esperado = 2
        self.assertEqual(resultado, esperado)  # testa se o chamado está em atendimento

    def test_encerrar_chamado(self):
        dados = {
            'atividades': 'Nenhuma'
        }
        caminho = reverse_lazy('encerrar_chamado', kwargs={'pk': self.chamado.pk})
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('index_tecnico_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        chamado = Chamado.objects.get(pk=self.chamado.pk)
        resultado = chamado.estado
        esperado = 3
        self.assertEqual(resultado, esperado)  # testa se o chamado foi encerrado

    def test_transferir_chamado_mesmo_nivel(self):
        dados = {
            'atividades': 'Nenhuma',
            'motivo_transferencia': 'Não tenho disponibilidade para atender',
            'tipo_transferencia': 'mesmo_nivel'
        }
        caminho = reverse_lazy('transferir_chamado', kwargs={'pk': self.chamado.pk})
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('index_tecnico_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        atendimentos = Atendimento.objects.filter(chamado=self.chamado)
        resultado = atendimentos.count()
        esperado = 2
        self.assertEqual(resultado, esperado)  # testa se foi criado um novo atendimento
        resultado = atendimentos[0].transferido
        esperado = True
        self.assertEqual(resultado, esperado)  # testa se o primeiro atendimento foi transferido
        resultado = atendimentos[1].tecnico.pk
        esperado = self.tecnico2.pk
        self.assertEqual(resultado, esperado)  # testa se o segundo atendimento foi alocado para o tecnico2

    def test_transferir_chamado_nivel_superior(self):
        dados = {
            'atividades': 'Nenhuma',
            'motivo_transferencia': 'Não tenho competência técnica para atender',
            'tipo_transferencia': 'nivel_superior'
        }
        caminho = reverse_lazy('transferir_chamado', kwargs={'pk': self.chamado.pk})
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('index_tecnico_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        atendimentos = Atendimento.objects.filter(chamado=self.chamado)
        resultado = atendimentos.count()
        esperado = 2
        self.assertEqual(resultado, esperado)  # testa se foi criado um novo atendimento
        resultado = atendimentos[0].transferido
        esperado = True
        self.assertEqual(resultado, esperado)  # testa se o primeiro atendimento foi transferido
        resultado = atendimentos[1].tecnico.pk
        esperado = self.tecnico3.pk
        self.assertEqual(resultado, esperado)  # testa se o segundo atendimento foi alocado para o tecnico2

    def test_transferir_chamado_nivel_superior_invalido(self):
        dados = {
            'atividades': 'Nenhuma',
            'motivo_transferencia': 'Não tenho competência técnica para atender',
            'tipo_transferencia': 'nivel_superior'
        }
        Usuario.objects.filter(nivel=1).delete()  # não tem mais usuários para transferir
        caminho = reverse_lazy('transferir_chamado', kwargs={'pk': self.chamado.pk})
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('index_tecnico_chamado')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        atendimentos = Atendimento.objects.filter(chamado=self.chamado)
        resultado = atendimentos.count()
        esperado = 1
        self.assertEqual(resultado, esperado)  # testa se não foi criado um novo atendimento
        resultado = atendimentos[0].transferido
        esperado = False
        self.assertEqual(resultado, esperado)  # testa se o atendimento não foi transferido

    def test_atualizar_localizacao(self):
        dados_enviados = {
            'latitude': '-23.5255246',
            'longitude':  '-46.6517839'
        }
        caminho = reverse_lazy('atualizar_localizacao')
        self.cliente_web.post(caminho, data=dados_enviados, format=dict)
        tecnico_autenticado = Usuario.objects.get(pk=self.tecnico1.pk)
        dados_recebidos = {
            'latitude': tecnico_autenticado.ultima_latitude,
            'longitude': tecnico_autenticado.ultima_longitude
        }
        self.assertDictEqual(dados_enviados, dados_recebidos)

    def test_atualizar_disponibilidade(self):
        dados_enviados = {
            'tecnico_ocupado': 'true'
        }
        caminho = reverse_lazy('atualizar_disponibilidade')
        self.cliente_web.post(caminho, data=dados_enviados, format=dict)
        tecnico_autenticado = Usuario.objects.get(pk=self.tecnico1.pk)
        resultado = tecnico_autenticado.tecnico_ocupado
        self.assertTrue(resultado)
