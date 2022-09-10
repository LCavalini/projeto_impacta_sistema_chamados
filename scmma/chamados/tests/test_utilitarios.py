from decimal import Decimal
from django.test import TestCase

from chamados.exceptions import CalculoDistanciaException, ConversaoEnderecoGeolocalizacaoException
from chamados.utilitarios import converter_endereco_geolocalizacao, calcular_distancia_pontos


class TestUtilitarios(TestCase):

    def test_converter_endereco_geolocalizacao_valido(self) -> None:
        endereco = 'Praça da Sé'
        esperado = (Decimal('-23.550389799999998'), Decimal('-46.633080956332904'))
        resultado = converter_endereco_geolocalizacao(endereco)
        self.assertEqual(resultado, esperado)

    def test_converter_endereco_geolocalizacao_sem_geolocalizacao(self) -> None:
        endereco = ''
        with self.assertRaises(ConversaoEnderecoGeolocalizacaoException):
            converter_endereco_geolocalizacao(endereco)

    def test_calcular_distancia_pontos_valido(self) -> None:
        inicio = (Decimal('-23.550389799999998'), Decimal('-46.633080956332904'))  # Praça da Sé
        final = (Decimal('-23.54541095'), Decimal('-46.63666383561214'))  # Vale do Anhangabaú
        esperado = Decimal('0.661731829778693')  # em km
        resultado = calcular_distancia_pontos(inicio, final)
        self.assertEqual(resultado, esperado)

    def test_calcular_distancia_pontos_sem_geolocalizacao(self) -> None:
        inicio = None  # não tem geolocalização
        final = (Decimal('-23.54541095'), Decimal('-46.63666383561214'))  # Vale do Anhangabaú
        with self.assertRaises(CalculoDistanciaException):
            calcular_distancia_pontos(inicio, final)
