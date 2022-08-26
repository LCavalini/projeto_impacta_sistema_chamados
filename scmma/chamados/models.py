from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractUser):
    TIPOS_USUARIOS = (
        (0, 'Cliente'),
        (1, 'Técnico'),
        (2, 'Administrador'),
    )
    CAMPOS_CLIENTE = ('email', 'first_name', 'last_name', 'data_nascimento', 'cpf', 'cnpj', 'telefone', )
    username = models.CharField('Nome de Usuário', max_length=150, null=True, blank=True)
    email = models.EmailField('Email', unique=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=30, null=True, blank=True)
    first_name = models.CharField('Nome', max_length=150, null=True)
    last_name = models.CharField('Sobrenome', max_length=150, null=True)
    _tipo_usuario = models.PositiveSmallIntegerField('Tipo de usuário', choices=TIPOS_USUARIOS, default=0,
                                                     db_column='tipo_usuario')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = GerenciadorUsuario()

    def get_fields_cliente(self) -> tuple:
        return [(field.verbose_name, field.value_from_object(self))
                for field in self.__class__._meta.fields if field.name in self.CAMPOS_CLIENTE]

    @property
    def tipo_usuario(self) -> str:
        return dict(self.TIPOS_USUARIOS)[self._tipo_usuario]

    @tipo_usuario.setter
    def tipo_usuario(self, valor):
        self._tipo_usuario = valor

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
    numero_serie = models.CharField('Número de série', max_length=50, unique=True)
    data_instalacao = models.DateField('Data de instalação', null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Cliente', null=True, blank=True)
    rua = models.CharField('Rua', max_length=100, null=True, blank=True)
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=100, null=True, blank=True)
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_FEDERACAO, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def get_fields(self) -> str:
        return [(field.verbose_name, field.value_from_object(self))
                for field in self.__class__._meta.fields if field.name in self.CAMPOS_TERMINAL]

    def __str__(self) -> str:
        return self.numero_serie


class Chamado(models.Model):
    ESTADOS = (
        (0, 'Aberto'),
        (1, 'Alocado'),
        (2, 'Transferido'),
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
    tipo = models.CharField('Tipo', choices=TIPOS_CHAMADO, max_length=100)
    descricao = models.TextField('Descrição')
    estado = models.PositiveSmallIntegerField('Estado', choices=ESTADOS, default=0)
    gravidade = models.PositiveSmallIntegerField('Gravidade', choices=NIVEIS_GRAVIDADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)

    @property
    def opcao_estado(self) -> str:
        return [item[1] for item in self.ESTADOS if item[0] == self.estado][0]
