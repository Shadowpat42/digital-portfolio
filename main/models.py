import re

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.db.models import Manager


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей, расширяющий BaseUserManager Django.
    Отвечает за создание и управление пользователями.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField("Email", max_length=30, unique=True)
    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField("Фамилия", max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

    @staticmethod
    def is_valid_email(email: str) -> bool:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MethodologicalResource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="methodological_files")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Media(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="video_and_image")
    media_type = models.CharField(
        max_length=10, choices=[("photo", "Photo"), ("video", "Video")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    HEART = "heart"
    FIRE = "fire"
    objects = models.Manager()

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (HEART, "Heart"),
        (FIRE, "Fire"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)  # Поле необязательно
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)  # Поле необязательно
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("user", "media", "post", "reaction_type")

    def __str__(self):
        return f"{self.user} - {self.reaction_type} - {self.media} - {self.post}"

