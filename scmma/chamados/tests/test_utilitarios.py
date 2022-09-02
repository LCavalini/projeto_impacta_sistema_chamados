from decimal import Decimal
from django.test import TestCase

from chamados.utilitarios import converter_endereco_geolocalizacao, calcular_distancia_pontos


class TestUtilitarios(TestCase):

    def test_converter_endereco_geolocalizacao(self):
        endereco = 'Praça da Sé'
        esperado = (Decimal('-23.550389799999998'), Decimal('-46.633080956332904'))
        resultado = converter_endereco_geolocalizacao(endereco)
        self.assertEqual(resultado, esperado)

    def test_calcular_distancia_pontos(self):
        inicio = (Decimal('-23.550389799999998'), Decimal('-46.633080956332904'))  # Praça da Sé
        final = (Decimal('-23.54541095'), Decimal('-46.63666383561214'))  # Vale do Anhangabaú
        esperado = Decimal('0.661731829778693')  # em km
        resultado = calcular_distancia_pontos(inicio, final)
        self.assertEqual(resultado, esperado)
