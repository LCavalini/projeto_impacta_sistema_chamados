from datetime import datetime
from django.test import TestCase

from chamados.exceptions import SemTecnicosDisponiveisException
from chamados.models import Usuario, Chamado, Terminal, Atendimento


class TestModelos(TestCase):

    def test_alocar_tecnico(self):
        cliente = Usuario(email='jsilva@gmail.com')
        cliente.tipo_usuario = 0
        cliente.save()
        terminal = Terminal(numero_serie='123', rua='Praça da Sé', bairro='Sé', cidade='São Paulo', estado='SP')
        terminal.save()
        chamado = Chamado(tipo=0, descricao='A máquina não inicializa', gravidade=1, usuario=cliente,
                          terminal=terminal)
        chamado.save()
        tecnico1 = Usuario(email='msilva@gmail.com', nivel=0)
        tecnico1.tipo_usuario = 1
        # Localização: Faculdade Impacta
        tecnico1.ultima_latitude, tecnico1.ultima_longitude = '-23.5255246', '-46.6517839'
        tecnico1.save()
        tecnico2 = Usuario(email='msantos@gmail.com', nivel=0)
        tecnico2.tipo_usuario = 1
        # Localização: Estádio do Morumbi
        tecnico2.ultima_latitude, tecnico2.ultima_longitude = '-23.6000839', '-46.7222789'
        tecnico2.save()
        tecnico3 = Usuario(email='cprado@gmail.com', nivel=0)
        tecnico3.tipo_usuario = 1
        # Localização: Vale do Anhangabaú
        tecnico3.ultima_latitude, tecnico3.ultima_longitude = '-23.5450214', '-46.6386695'
        tecnico3.tecnico_ocupado = True
        tecnico3.save()
        atendimento = Atendimento(chamado=chamado)
        atendimento.alocar_tecnico()
        atendimento.save()
        resultado = atendimento.tecnico.email
        esperado = tecnico1.email  # técnico mais próximo e não ocupado
        self.assertEqual(resultado, esperado)

    def test_gerar_numero_protocolo(self) -> None:
        agora = datetime.now()
        dia, mes, ano = agora.day, agora.month, agora.year
        cliente = Usuario(email='cliente@cliente.com')
        cliente.save()
        terminal = Terminal(numero_serie='123')
        terminal.save()
        chamado1 = Chamado(tipo='erro_leitura_cartao', descricao='Sem descrição', gravidade=1, usuario=cliente,
                           terminal=terminal)
        chamado1.protocolo = Chamado.objects.gerar_numero_protocolo()
        chamado1.save()
        resultado = chamado1.protocolo
        esperado = f'{ano:04d}{mes:02d}{dia:02d}{1:06d}'
        self.assertEqual(resultado, esperado)
        chamado2 = Chamado(tipo='erro_leitura_cartao', descricao='Sem descrição', gravidade=1, usuario=cliente,
                           terminal=terminal)
        chamado2.protocolo = Chamado.objects.gerar_numero_protocolo()
        chamado2.save()
        resultado = chamado2.protocolo
        esperado = f'{ano:04d}{mes:02d}{dia:02d}{2:06d}'
        self.assertEqual(resultado, esperado)

    def test_create_chamado_valido(self) -> None:
        """
        Testa se a função create_chamado cria um chamado e um atendimento relacionado.
        """
        cliente = Usuario(email='jsilva@gmail.com')
        cliente.tipo_usuario = 0
        cliente.save()
        terminal = Terminal(numero_serie='123', rua='Praça da Sé', bairro='Sé', cidade='São Paulo', estado='SP')
        terminal.save()
        tecnico = Usuario(email='msilva@gmail.com', nivel=0)
        tecnico.tipo_usuario = 1
        # Localização: Faculdade Impacta
        tecnico.ultima_latitude, tecnico.ultima_longitude = '-23.5255246', '-46.6517839'
        tecnico.save()
        dados_chamado = {
            'tipo': 'erro_leitura_cartao',
            'descricao': 'Sem descrição',
            'gravidade': 1,
            'usuario': cliente,
            'terminal': terminal
        }
        chamado = Chamado.objects.create_chamado(**dados_chamado)
        chamado.save()
        atendimento = Atendimento.objects.filter(chamado=chamado).last()
        resultado = atendimento.tecnico.email
        esperado = tecnico.email
        self.assertEqual(resultado, esperado)

    def test_create_chamado_invalido(self) -> None:
        cliente = Usuario(email='jsilva@gmail.com')
        cliente.tipo_usuario = 0
        cliente.save()
        terminal = Terminal(numero_serie='123', rua='Praça da Sé', bairro='Sé', cidade='São Paulo', estado='SP')
        terminal.save()
        # O técnico é de nível 1 e não pode receber o chamado
        tecnico = Usuario(email='msilva@gmail.com', nivel=1)
        tecnico.tipo_usuario = 1
        tecnico.save()
        dados_chamado = {
            'tipo': 'erro_leitura_cartao',
            'descricao': 'Sem descrição',
            'gravidade': 1,
            'usuario': cliente,
            'terminal': terminal
        }
        with self.assertRaises(SemTecnicosDisponiveisException):
            Chamado.objects.create_chamado(**dados_chamado)
