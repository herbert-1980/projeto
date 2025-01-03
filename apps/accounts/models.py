from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import re


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Usuários devem ter um endereço de email')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # Novo campo
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # Gerar username a partir do email (sem caracteres especiais)
        get_email = self.email.split("@")[0]
        self.username = re.sub(r"[^a-zA-Z0-9]", "", get_email)

        # verificar se o username já existe
        count = 1
        original_username = self.username
        while MyUser.objects.filter(username=self.username).exists():
            self.username = f"{original_username}{count}"
            count += 1

        # Validação extra para garantir que o username não está vazio
        if not self.username:
            raise ValidationError("Username não pode ser vazio.")

        super(MyUser, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"