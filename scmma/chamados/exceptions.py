class CalculoDistanciaException(Exception):

    def __init__(self, message: str = 'Erro ao calcular a distância de dois pontos') -> None:
        super().__init__(message)


class SemTecnicosDisponiveisException(Exception):

    def __init__(self, message: str = 'Não há técnicos disponíveis') -> None:
        super().__init__(message)
