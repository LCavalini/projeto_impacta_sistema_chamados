from django.test import TestCase

from chamados.models import Usuario, Chamado, Terminal, Atendimento


class TestModelos(TestCase):

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
