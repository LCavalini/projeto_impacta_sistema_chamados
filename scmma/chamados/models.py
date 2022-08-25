from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class GerenciadorUsuario(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        usuario = self.model(
            email=self.normalize_email(email),
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None):
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
        (2, 'Administrador')
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

    def get_fields_cliente(self):
        return [(field.verbose_name, field.value_from_object(self))
                for field in self.__class__._meta.fields if field.name in self.CAMPOS_CLIENTE]

    @property
    def tipo_usuario(self):
        return dict(self.TIPOS_USUARIOS)[self._tipo_usuario]

    @tipo_usuario.setter
    def tipo_usuario(self, valor):
        self._tipo_usuario = valor

    def __str__(self):
        return self.get_full_name()


class Terminal(models.Model):
    CAMPOS_TERMINAL = ('numero_serie', 'data_instalacao', 'usuario', 'rua', 'numero', 'bairro', 'complemento', 'cep',
                       'cidade', 'estado', )
    data_instalacao = models.DateField('Data de instalação', null=True, blank=True)
    numero_serie = models.CharField('Número de série', max_length=50, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Cliente', null=True, blank=True)
    rua = models.CharField('Rua', max_length=100, null=True, blank=True)
    numero = models.CharField('Número', max_length=10, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=100, null=True, blank=True)
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    estado = models.CharField('Estado', max_length=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self))
                for field in self.__class__._meta.fields if field.name in self.CAMPOS_TERMINAL]

    def __str__(self):
        return self.numero_serie


class Chamado(models.Model):
    ESTADOS = (
        (0, 'aberto'),
        (1, 'alocado'),
        (2, 'transferido'),
        (3, 'encerrado'),
    )
    NIVEIS_GRAVIDADE = (
        (0, 'baixa'),
        (1, 'média'),
        (2, 'alta'),
    )
    descricao = models.TextField('Descrição')
    estado = models.PositiveSmallIntegerField('Estado', choices=ESTADOS, default=0)
    tipo = models.CharField('Tipo', max_length=100)
    gravidade = models.PositiveSmallIntegerField('Gravidade', choices=NIVEIS_GRAVIDADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)

    @property
    def opcao_estado(self):
        return [item[1] for item in self.ESTADOS if item[0] == self.estado][0]
