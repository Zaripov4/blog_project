from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_on__isnull=True)


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(auto_now=True, db_index=True)
    deleted_on = models.DateTimeField(null=True, blank=True, default=None)

    objects = BaseManager()
    objects_all = models.Manager()

    class Meta:
        abstract = True
        ordering = ['created_on']

    def mark_deleted(self):
        self.deleted_on = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not all([username, email, password]):
            raise ValidationError(
                {'detail': 'Required fields email, username and password'}
            )
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, *args, **kwargs):
        user = self.create_user(password=password, *args, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser, BaseModel):
    id = models.AutoField(primary_key=True, editable=False)
    password = models.CharField(_('password'), max_length=128)
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class ResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user']

    def save(self, *args, **kwargs):
        ResetCode.objects.filter(user=self.user).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email
