from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models, transaction
from typing import Union

from .exceptions import SemTecnicosDisponiveisException, CalculoDistanciaException
from .utilitarios import converter_endereco_geolocalizacao, calcular_distancia_pontos


class GerenciadorUsuario(BaseUserManager):
    """
    Gerenciamento de usuários baseado nos campos email (em vez de username) e password.
    """

    def create_user(self, email, password=None) -> AbstractUser:
        if not email:
            raise ValueError('Email é um campo obrigatório')
        usuario = self.model(
            email=self.normalize_email(email),
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None) -> AbstractUser:
        usuario = self.create_user(
            email,
            password=password,
        )
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.tipo_usuario = 2  # Usuário do tipo Administrador
        usuario.first_name = 'Administrador'
        usuario.last_name = 'Geral'
        usuario.save(using=self._db)
        return usuario


class GerenciadorChamado(models.Manager):

    def create_chamado(self, **kwargs) -> models.Model:
        try:
            with transaction.atomic():
                chamado = self.create(**kwargs)
                atendimento = Atendimento.objects.create_atendimento(chamado=chamado)
                atendimento.save()
                chamado.estado = 1  # se o atendimento for criado, o chamado muda o estado para 'Alocado'
                chamado.protocolo = self.gerar_numero_protocolo()
        except Exception as e:
            raise e
        return chamado

    def gerar_numero_protocolo(self) -> str:
        """
        Gera e retorna um número de protocolo com o seguinte formato: AAAAMMDDXXXXXX, sendo AAAA o ano, MM o mês e DD o
        dia da abertura do chamado e XXXXX um número de sequência crescente dos chamados abertos no dia.
        """
        agora = datetime.now()
        ano, mes, dia = agora.year, agora.month, agora.day
        prefixo_protocolo = f'{ano:04d}{mes:02d}{dia:02d}'
        ultimo_chamado_hoje = Chamado.objects.filter(protocolo__startswith=prefixo_protocolo).last()
        if not ultimo_chamado_hoje:
            sufixo_protocolo = f'{1:06d}'  # se não houver chamado na mesma data, inicia a sequência em 1
        else:
            ultimo_numero = int(ultimo_chamado_hoje.protocolo.replace(prefixo_protocolo, ''))
            sufixo_protocolo = f'{ultimo_numero + 1:06d}'
        return f'{prefixo_protocolo}{sufixo_protocolo}'


class GerenciadorAtendimento(models.Manager):

    def create_atendimento(self, **kwargs) -> models.Model:
        """
        Cria um registro de atendimento.

        Parâmetros
        ----------
        nivel: int
            Nível do técnico que deverá ser alocado para o atendimento.
            Padrão: 0 [Nível 1].

        ignorar_tecnicos: list
            Lista de técnicos que não devem ser alocados para o atendimento. Geralmente, é o técnico que transferiu
            o chamado.
            Padrão: [].
        """
        nivel = kwargs.pop('nivel', 0)
        ignorar_tecnicos = kwargs.pop('ignorar_tecnicos', [])
        try:
            with transaction.atomic():
                atendimento = self.create(**kwargs)
                atendimento.alocar_tecnico(nivel=nivel, ignorar_tecnicos=ignorar_tecnicos)
        except Exception as e:
            raise e
        return atendimento


class Usuario(AbstractUser):
    TIPOS_USUARIOS = (
        (0, 'Cliente', ),
        (1, 'Técnico', ),
        (2, 'Administrador', ),
    )
    OPCOES_NIVEIS = (
        (0, 'Nível 1', ),
        (1, 'Nível 2',),
        (2, 'Nível 3', ),
    )
    CAMPOS_CLIENTE = ('email', 'first_name', 'last_name', 'data_nascimento', 'cpf', 'cnpj', 'telefone', )
    CAMPOS_TECNICO = ('email', 'first_name', 'last_name', 'data_nascimento', 'cpf', 'telefone', 'nivel', )
    username = models.CharField('Nome de Usuário', max_length=150, null=True, blank=True)
    email = models.EmailField('Email', unique=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=15, null=True, blank=True)
    first_name = models.CharField('Nome', max_length=150, null=True)
    last_name = models.CharField('Sobrenome', max_length=150, null=True)
    _tipo_usuario = models.PositiveSmallIntegerField('Tipo de usuário', choices=TIPOS_USUARIOS, default=0,
                                                     db_column='tipo_usuario')
    nivel = models.PositiveSmallIntegerField('Nível', choices=OPCOES_NIVEIS, null=True)
    ultima_latitude = models.CharField('Última latitude', max_length=50, null=True, blank=True)
    ultima_longitude = models.CharField('Última longitude', max_length=50, null=True, blank=True)
    tecnico_ocupado = models.BooleanField('Tecnico ocupado?', default=False)
    USERNAME_FIELD = 'email'  # o nome de usuário é o email
    REQUIRED_FIELDS = []
    objects = GerenciadorUsuario()

    @property
    def tipo_usuario(self) -> str:
        return dict(self.TIPOS_USUARIOS)[self._tipo_usuario]

    @tipo_usuario.setter
    def tipo_usuario(self, valor):
        self._tipo_usuario = valor

    @property
    def geolocalizacao(self):
        try:
            return (Decimal(self.ultima_latitude), Decimal(self.ultima_longitude))
        except Exception:
            return None

    @property
    def campos(self) -> tuple:
        campos = self.CAMPOS_CLIENTE if self.tipo_usuario == 'Cliente' else self.CAMPOS_TECNICO
        campos_valor = []
        for campo in self.__class__._meta.fields:
            nome_campo = campo.verbose_name
            valor = campo.value_from_object(self)
            if campo.name not in campos:
                continue
            if campo.name == 'nivel':
                valor = dict(self.OPCOES_NIVEIS)[valor]
            campos_valor.append((nome_campo, valor))
        return campos_valor

    def __str__(self) -> str:
        return self.get_full_name()


class Terminal(models.Model):
    CAMPOS_TERMINAL = ('numero_serie', 'data_instalacao', 'usuario', 'rua', 'numero', 'bairro', 'complemento', 'cep',
                       'cidade', 'estado', )
    ESTADOS_FEDERACAO = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('MT', 'Mato Grosso'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )
    CAMPOS_ENDERECO = ('rua', 'numero', 'bairro', 'cep', 'cidade', 'estado', )
    numero_serie = models.CharField('Número de série', max_length=50, unique=True)
    data_instalacao = models.DateField('Data de instalação', null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Cliente', null=True, blank=True)
    rua = models.CharField('Rua', max_length=100, null=True, blank=True)
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=100, null=True, blank=True)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_FEDERACAO, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    latitude = models.CharField('Latitude', max_length=50, null=True, blank=True)
    longitude = models.CharField('Longitude', max_length=50, null=True, blank=True)

    @property
    def geolocalizacao(self) -> Union[tuple, None]:
        try:
            return (Decimal(self.latitude), Decimal(self.longitude))
        except Exception:
            return None

    @property
    def campos(self) -> list:
        campos_valor = []
        for campo in self.__class__._meta.fields:
            nome_campo = campo.verbose_name
            valor = campo.value_from_object(self)
            if campo.name not in self.CAMPOS_TERMINAL:
                continue
            if campo.name == 'usuario':
                valor = self.usuario.get_full_name()
            campos_valor.append((nome_campo, valor))
        return campos_valor

    def configurar_geolocalizacao(self):
        """
        Define os dados de geolocalização (latitude e longitude) por meio da consulta dos campos de endereço.
        """
        endereco = ' '.join([getattr(self, campo) for campo in self.CAMPOS_ENDERECO if getattr(self, campo)])
        geolocalizacao = converter_endereco_geolocalizacao(endereco)
        if geolocalizacao:
            self.latitude, self.longitude = geolocalizacao

    def __str__(self) -> str:
        return self.numero_serie


class Chamado(models.Model):
    ESTADOS = (
        (0, 'Aberto'),
        (1, 'Alocado'),
        (2, 'Em atendimento'),
        (3, 'Encerrado'),
    )
    NIVEIS_GRAVIDADE = (
        (0, 'Baixa'),
        (1, 'Média'),
        (2, 'Alta'),
    )
    TIPOS_CHAMADO = (
        ('maquina_nao_inicializa', 'Máquina não inicializa'),
        ('erro_leitura_cartao', 'Erro de leitura de cartão'),
        ('erro_pagamento', 'Erro ao efetuar o pagamento'),
        ('outros', 'Outros')
    )
    protocolo = models.CharField('Protocolo', max_length=14)
    tipo = models.CharField('Tipo', choices=TIPOS_CHAMADO, max_length=100)
    descricao = models.TextField('Descrição')
    estado = models.PositiveSmallIntegerField('Estado', choices=ESTADOS, default=0)
    gravidade = models.PositiveSmallIntegerField('Gravidade', choices=NIVEIS_GRAVIDADE)
    usuario = models.ForeignKey(Usuario, verbose_name='Cliente', on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, verbose_name='Terminal', on_delete=models.CASCADE)
    objects = GerenciadorChamado()

    @property
    def opcao_estado(self) -> str:
        return [item[1] for item in self.ESTADOS if item[0] == self.estado][0]

    def campos(self) -> list:
        return [
            ('Tipo', dict(self.TIPOS_CHAMADO)[self.tipo]),
            ('Descrição', self.descricao),
            ('Estado', dict(self.ESTADOS)[self.estado]),
            ('Gravidade', dict(self.NIVEIS_GRAVIDADE)[self.gravidade]),
            ('Cliente', self.usuario),
            ('Terminal', self.terminal),
            ('Rua', self.terminal.rua),
            ('Número', self.terminal.numero),
            ('Complemento', self.terminal.complemento),
            ('Bairro', self.terminal.bairro),
            ('Cidade', self.terminal.cidade),
            ('Estado', dict(self.terminal.ESTADOS_FEDERACAO)[self.terminal.estado]),
            ('CEP', self.terminal.cep)
        ]


class Atendimento(models.Model):
    tecnico = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    atividades = models.TextField('Atividades realizadas', null=True)
    transferido = models.BooleanField('Atendimento transferido', default=False)
    motivo_transferencia = models.TextField('Motivo da transferencia', null=True)
    objects = GerenciadorAtendimento()

    def alocar_tecnico(self, nivel: int = 0, ignorar_tecnicos: list = []):
        """
        Aloca um técnico para o atendimento seguindo critérios de disponibilidade e de proximidade (geolocalização).
        """
        tecnicos = Usuario.objects.filter(_tipo_usuario=1, nivel=nivel, is_active=True)
        tecnicos_com_geolocalizacao = []
        tecnicos_sem_geolocalizacao = []
        self.chamado.terminal.configurar_geolocalizacao()
        for tecnico in tecnicos:
            if tecnico in ignorar_tecnicos:
                continue
            try:
                distancia = calcular_distancia_pontos(tecnico.geolocalizacao, self.chamado.terminal.geolocalizacao)
                tecnicos_com_geolocalizacao.append((tecnico, tecnico.tecnico_ocupado, distancia))
            except CalculoDistanciaException:
                tecnicos_sem_geolocalizacao.append((tecnico, tecnico.tecnico_ocupado, None))
        # os técnicos com geolocalização são ordenados pela disponibilidade e distância em relação ao terminal
        tecnicos_com_geolocalizacao = sorted(tecnicos_com_geolocalizacao, key=lambda x: (x[1], x[2]))
        # os técnicos sem geolocalização são ordenados apenas pela disponibilidade
        tecnicos_sem_geolocalizacao = sorted(tecnicos_sem_geolocalizacao, key=lambda x: (x[1]))
        tecnicos_ordenados = tecnicos_com_geolocalizacao
        # os técnicos sem geolocalização ficam no final da lista
        tecnicos_ordenados.extend(tecnicos_sem_geolocalizacao)
        if len(tecnicos_ordenados) < 1:
            raise SemTecnicosDisponiveisException()
        self.tecnico = tecnicos_ordenados[0][0]

    def campos(self) -> list:
        return [
            ('Técnico', self.tecnico),
            ('Atividades', self.atividades),
            ('Transferido?', 'Sim' if self.transferido else 'Não'),
            ('Motivo da transferência', self.motivo_transferencia),
        ]
