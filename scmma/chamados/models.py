from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class GerenciadorUsuario(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractUser):
    USER_TYPES = (
        (0, 'Cliente'),
        (1, 'Técnico'),
    )
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    birth_date = models.DateField('Data de nascimento', null=True)
    cpf = models.CharField('CPF', max_length=11, null=True)
    cnpj = models.CharField('CNPJ', max_length=14, null=True)
    telefone = models.CharField('Telefone', max_length=30, null=True)
    user_type = models.BinaryField('Tipo de usuário', choices=USER_TYPES, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = GerenciadorUsuario()

    def campos(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.get_full_name()


class Terminal(models.Model):
    data_instalacao = models.DateField('Data de instalação')
    numero_serie = models.CharField('Número de série', max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def campos(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)

    @property
    def opcao_estado(self):
        return [item[1] for item in self.ESTADOS if item[0] == self.estado][0]
