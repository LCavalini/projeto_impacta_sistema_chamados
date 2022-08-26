from django.test import Client, TestCase
from django.urls import reverse_lazy

from chamados.models import Terminal, Usuario


class TestCadastramentoTerminal(TestCase):

    def setUp(self) -> None:
        self.cliente_web = Client()
        self.admin = Usuario(email='admin@admin.com', password='123', is_superuser=True)
        self.admin.save()
        self.cliente_web.force_login(self.admin)

    def test_adicionar_terminal_valido(self) -> None:
        dados = {
            'numero_serie': '123',
            'data_instalacao': '2022-05-08'
        }
        caminho = reverse_lazy('adicionar_terminal')
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('admin_index_terminal')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        terminal = Terminal.objects.get(numero_serie=dados['numero_serie'])
        resultado = terminal.data_instalacao
        esperado = dados['data_instalacao']
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_adicionar_terminal_invalido(self) -> None:
        dados = {
            'numero_serie': '123',
            'data_instalacao': '2022-08'
        }
        caminho = reverse_lazy('adicionar_terminal')
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta.status_code
        esperado = 200
        self.assertEqual(resultado, esperado)  # teste da requisição
        with self.assertRaises(Terminal.DoesNotExist):  # não pode ter criado o terminal
            Terminal.objects.get(numero_serie=dados['numero_serie'])

    def test_editar_terminal_valido(self) -> None:
        dados_criacao = {
            'numero_serie': '123',
            'data_instalacao': '2022-08-05',  # o modelo usa o formato YYYY-MM-DD
            'rua': 'Praça da Sé',
            'numero': 's/n',
            'complemento': 'Estação da Sé - Piso Térreo - Entrada',
            'bairro': 'Sé',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01310200'
        }
        dados_edicao = {
            'numero_serie': '123',
            'data_instalacao': '2022-08-05',
            'rua': 'Praça da Sé',
            'numero': 's/n',
            'complemento': 'Estação da Sé - Piso Térreo - Próx. Bilheteria',
            'bairro': 'Sé',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01310200'
        }
        terminal_criado = Terminal(**dados_criacao)
        terminal_criado.save()
        pk = Terminal.objects.get(numero_serie=dados_criacao['numero_serie']).pk
        caminho = reverse_lazy('editar_terminal', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho, data=dados_edicao, format=dict)
        resultado = resposta
        esperado = reverse_lazy('admin_index_terminal')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        terminal_editado = Terminal.objects.get(numero_serie=dados_criacao['numero_serie'])
        resultado = terminal_editado.complemento
        esperado = dados_edicao['complemento']
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_editar_terminal_invalido(self) -> None:
        dados_criacao = {
            'numero_serie': '123',
            'data_instalacao': '2022-08-05',  # o modelo usa o formato YYYY-MM-DD
            'rua': 'Praça da Sé',
            'numero': 's/n',
            'complemento': 'Estação da Sé - Piso Térreo - Entrada',
            'bairro': 'Sé',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01310200'
        }
        dados_edicao = {
            'numero_serie': '123',
            'data_instalacao': '2022-08-05',
            'rua': 'Praça da Sé',
            'numero': 's/n',
            'complemento': 'Estação da Sé - Piso Térreo - Entrada',
            'bairro': 'Sé',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '013102000'  # cep inválido
        }
        terminal_criado = Terminal(**dados_criacao)
        terminal_criado.save()
        pk = Terminal.objects.get(numero_serie=dados_criacao['numero_serie']).pk
        caminho = reverse_lazy('editar_terminal', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho, data=dados_edicao, format=dict)
        resultado = resposta.status_code
        esperado = 200
        self.assertEqual(resultado, esperado)  # teste da requisição
        terminal_editado = Terminal.objects.get(numero_serie=dados_criacao['numero_serie'])
        resultado = terminal_editado.cep
        esperado = dados_criacao['cep']
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_remover_terminal_valido(self) -> None:
        dados = {
            'numero_serie': '123'
        }
        terminal_criado = Terminal(**dados)
        terminal_criado.save()
        pk = Terminal.objects.get(numero_serie=dados['numero_serie']).pk
        caminho = reverse_lazy('remover_terminal', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho)
        resultado = resposta
        esperado = reverse_lazy('admin_index_terminal')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        resultado = Terminal.objects.get(numero_serie=dados['numero_serie']).is_active
        self.assertFalse(resultado)  # teste de banco de dados

    def test_reativar_terminal_valido(self) -> None:
        dados = {
            'numero_serie': '123',
            'is_active': False
        }
        terminal_criado = Terminal(**dados)
        terminal_criado.save()
        terminal_criado = Terminal.objects.get(numero_serie=dados['numero_serie'])
        pk = terminal_criado.pk
        resultado = terminal_criado.is_active
        self.assertFalse(resultado)  # o atributo deve ter sido gravado como falso
        caminho = reverse_lazy('reativar_terminal', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho)
        resultado = resposta
        esperado = reverse_lazy('admin_index_terminal')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        resultado = Terminal.objects.get(numero_serie=dados['numero_serie']).is_active
        self.assertTrue(resultado)  # teste de banco de dados
