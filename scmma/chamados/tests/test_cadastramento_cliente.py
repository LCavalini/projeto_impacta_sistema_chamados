from django.test import Client, TestCase
from django.urls import reverse_lazy

from chamados.models import Usuario


class TestCadastramentoCliente(TestCase):

    def setUp(self) -> None:
        self.cliente_web = Client()
        self.admin = Usuario(email='admin@admin.com', password='123', is_superuser=True)
        self.admin.save()
        self.cliente_web.force_login(self.admin)

    def test_adicionar_cliente_valido(self) -> None:
        dados = {
            'email': 'joao.silva@gmail.com',
            'first_name': 'João',
            'last_name': 'Silva',
            'data_nascimento': '',
            'cpf': '',
            'cnpj': '',
            'telefone': ''
        }
        caminho = reverse_lazy('adicionar_cliente')
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('admin_index_cliente')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        usuario = Usuario.objects.get(email=dados['email'])
        resultado = usuario.get_full_name()
        esperado = ' '.join([dados['first_name'], dados['last_name']])
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_adicionar_cliente_email_invalido(self) -> None:
        dados = {
            'email': 'joao.silvagmail.com',
            'first_name': 'João',
            'last_name': 'Silva',
            'data_nascimento': '',
            'cpf': '',
            'cnpj': '',
            'telefone': ''
        }
        caminho = reverse_lazy('adicionar_cliente')
        resposta = self.cliente_web.post(caminho, data=dados, format=dict)
        resultado = resposta.status_code
        esperado = 200
        self.assertEqual(resultado, esperado)  # teste da requisição (deve retornar a própria página)
        with self.assertRaises(Usuario.DoesNotExist):  # não pode ter criado o cliente
            Usuario.objects.get(email=dados['email'])

    def test_editar_cliente_valido(self) -> None:
        dados_criacao = {
            'email': 'maria.silva@gmail.com',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'data_nascimento': '1953-08-05',  # o modelo usa o formato YYYY-MM-DD
            'cpf': '87955321421',
            'cnpj': '',
            'telefone': '1132152317'
        }
        dados_edicao = {
            'email': 'maria.silva@gmail.com',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'data_nascimento': '1953-08-05',  # o modelo usa o formato YYYY-MM-DD
            'cpf': '87955321421',
            'cnpj': '',
            'telefone': '11985412310'
        }
        usuario_criado = Usuario(**dados_criacao)
        usuario_criado.save()
        pk = Usuario.objects.get(email=dados_criacao['email']).pk
        caminho = reverse_lazy('editar_cliente', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho, data=dados_edicao, format=dict)
        resultado = resposta
        esperado = reverse_lazy('admin_index_cliente')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        usuario_editado = Usuario.objects.get(email=dados_criacao['email'])
        resultado = usuario_editado.telefone
        esperado = dados_edicao['telefone']
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_editar_cliente_email_invalido(self) -> None:
        dados_criacao = {
            'email': 'maria.silva@gmail.com',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'data_nascimento': '1953-08-05',  # o modelo usa o formato YYYY-MM-DD
            'cpf': '87955321421',
            'cnpj': '',
            'telefone': '1132152317'
        }
        dados_edicao = {
            'email': 'maria.silva',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'data_nascimento': '1953-08-05',  # o modelo usa o formato YYYY-MM-DD
            'cpf': '87955321421',
            'cnpj': '',
            'telefone': '11985412310'
        }
        usuario_criado = Usuario(**dados_criacao)
        usuario_criado.save()
        pk = Usuario.objects.get(email=dados_criacao['email']).pk
        caminho = reverse_lazy('editar_cliente', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho, data=dados_edicao, format=dict)
        resultado = resposta.status_code
        esperado = 200
        self.assertEqual(resultado, esperado)  # teste da requisição (retorna a própria página)
        usuario_editado = Usuario.objects.get(email=dados_criacao['email'])
        resultado = usuario_editado.telefone
        esperado = dados_criacao['telefone']
        self.assertEqual(resultado, esperado)  # teste de banco de dados (telefone não pode ter sido alterado)

    def test_remover_cliente_valido(self) -> None:
        dados = {
            'email': 'marcos.silva@gmail.com',
            'first_name': 'Marcos',
            'last_name': 'Silva',
        }
        usuario_criado = Usuario(**dados)
        usuario_criado.save()
        pk = Usuario.objects.get(email=dados['email']).pk
        caminho = reverse_lazy('remover_cliente', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho)
        resultado = resposta
        esperado = reverse_lazy('admin_index_cliente')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        resultado = Usuario.objects.get(email=dados['email']).is_active
        self.assertFalse(resultado)  # teste de banco de dados

    def test_reativar_cliente_valido(self):
        dados = {
            'email': 'luis.silva@gmail.com',
            'first_name': 'Luis',
            'last_name': 'Silva',
            'is_active': False
        }
        usuario_criado = Usuario(**dados)
        usuario_criado.save()
        usuario_criado = Usuario.objects.get(email=dados['email'])
        pk = usuario_criado.pk
        resultado = usuario_criado.is_active  # o atributo deve ter sido gravado como falso
        self.assertFalse(resultado)
        caminho = reverse_lazy('reativar_cliente', kwargs={'pk': pk})
        resposta = self.cliente_web.post(caminho)
        resultado = resposta
        esperado = reverse_lazy('admin_index_cliente')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        resultado = Usuario.objects.get(email=dados['email']).is_active
        self.assertTrue(resultado)  # teste de banco de dados
