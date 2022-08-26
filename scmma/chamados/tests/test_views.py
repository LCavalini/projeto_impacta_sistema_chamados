from django.test import Client, TestCase
from chamados.models import Usuario
from django.urls import reverse_lazy


class TestAdicionarCliente(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.admin = Usuario(email='admin@admin.com', password='123', is_superuser=True)
        self.admin.save()
        self.cliente.force_login(self.admin)

    def test_adicionar_cliente_valido(self):
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
        resposta = self.cliente.post(caminho, data=dados, format=dict)
        resultado = resposta
        esperado = reverse_lazy('admin_index_cliente')
        self.assertRedirects(resultado, esperado)  # teste da requisição
        usuario = Usuario.objects.get(email=dados['email'])
        resultado = usuario.get_full_name()
        esperado = 'João Silva'
        self.assertEqual(resultado, esperado)  # teste de banco de dados

    def test_adicionar_cliente_email_invalido(self):
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
        resposta = self.cliente.post(caminho, data=dados, format=dict)
        resultado = resposta.status_code
        esperado = 200
        self.assertEqual(resultado, esperado)  # teste da requisição (deve retornar a página)
        with self.assertRaises(Usuario.DoesNotExist):  # não pode ter criado o cliente
            usuario = Usuario.objects.get(email=dados['email'])
            resultado = usuario.get_full_name()
