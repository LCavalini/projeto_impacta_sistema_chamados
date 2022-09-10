class CalculoDistanciaException(Exception):

    def __init__(self, message: str = 'erro ao calcular a distância de dois pontos') -> None:
        super().__init__(message)


class ConversaoEnderecoGeolocalizacaoException(Exception):

    def __init__(self, message: str = 'erro ao converter o endereço em geolocalização') -> None:
        super().__init__(message)


class SemTecnicosDisponiveisException(Exception):

    def __init__(self, message: str = 'não há técnicos disponíveis') -> None:
        super().__init__(message)


class ConfiguracaoGeolocalizacaoException(Exception):

    def __init__(self, message: str = 'Erro ao localizar o endereço') -> None:
        super().__init__(message)
