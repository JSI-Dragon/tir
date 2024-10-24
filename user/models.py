from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Требуется электронная почта')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя', max_length=123)
    email = models.EmailField('Электронная почта', blank=True, null=True, unique=True)
    phone_number = models.CharField('Номер телефона', max_length=17)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления', auto_now=True)
    avatar = models.ImageField('Аватарка', upload_to='avatars/', blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер'),
            (3, 'Консультант'),
            (4, 'Администратор'),
            (5, 'Автор туру'),
        ),
        default=1,
        verbose_name='Роль пользователя'
    )
    is_admin = models.BooleanField('Является администратором', default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField('Заблокирован', default=False)

    favorite_tours = models.ManyToManyField('tour.Tour', related_name='favorited_by_users', blank=True)
    bookings = models.ManyToManyField('tour.Booking', blank=True, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_admin 

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'