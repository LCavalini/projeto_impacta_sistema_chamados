from django.test import TestCase

from chamados.models import Usuario, Chamado, Terminal, Atendimento


class TestModelos(TestCase):

    """
    def test_tecnico_ocupado(self) -> None:
        cliente = Usuario(email='msilva@gmail.com')
        cliente.save()
        tecnico = Usuario(email='jsilva@gmail.com')
        tecnico.save()
        terminal = Terminal(numero_serie='123')
        terminal.save()
        # chamado em atendimento
        chamado = Chamado(usuario=cliente, terminal=terminal, gravidade=0, estado=2)
        chamado.save()
        atendimento = Atendimento(tecnico=tecnico, chamado=chamado)
        atendimento.save()
        self.assertTrue(tecnico.tecnico_ocupado())

    def test_tecnico_nao_ocupado(self) -> None:
        cliente = Usuario(email='msilva@gmail.com')
        cliente.save()
        tecnico = Usuario(email='jsilva@gmail.com')
        tecnico.save()
        terminal = Terminal(numero_serie='123')
        terminal.save()
        # chamado apenas alocado
        chamado = Chamado(usuario=cliente, terminal=terminal, gravidade=0, estado=1)
        chamado.save()
        atendimento = Atendimento(tecnico=tecnico, chamado=chamado)
        atendimento.save()
        # o chamado não está em atendimento
        self.assertFalse(tecnico.tecnico_ocupado())
        chamado.estado = 2
        chamado.save()
        atendimento.transferido = True
        atendimento.save()
        # o chamado foi transferido
        self.assertFalse(tecnico.tecnico_ocupado())
        outro_tecnico = Usuario(email='jsantos@gmail.com')
        outro_tecnico.save()
        atendimento.tecnico = outro_tecnico
        atendimento.transferido = False
        atendimento.save()
        # o técnico não tem chamados
        self.assertFalse(tecnico.tecnico_ocupado())
    """

    def test_alocar_tecnico(self):
        cliente = Usuario(email='jsilva@gmail.com')
        cliente.tipo_usuario = 0
        cliente.save()
        terminal = Terminal(numero_serie='123', rua='Praça da Sé', bairro='Sé', cidade='São Paulo', estado='SP')
        terminal.configurar_geolocalizacao()
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
