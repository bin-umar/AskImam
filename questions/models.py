from django.shortcuts import reverse
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

# Create your models here.
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0)
    answer_count = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    votes = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    tags = models.ManyToManyField(to='Tag', related_name='questions')

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})


class Tag(models.Model):
    text = models.SlugField(unique=True)


class Answer(models.Model):
    # Ответ – содержание, автор, дата написания, флаг правильного ответа, рейтинг.
    text = HTMLField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0)
    record_date = models.DateTimeField(auto_now_add=True)
    is_true = models.BooleanField()
    votes = models.DecimalField(max_digits=10, decimal_places=0, default=0)
# # Пользователь – электронная почта, никнейм, пароль, аватарка, дата регистрации, рейтинг.
# class MyUserManager(BaseUserManager):
#     def create_user(self,  username, email, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, email, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             username=username,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
# class MyUser(AbstractBaseUser):
#     username = models.CharField(max_length=20, unique=True)
#     nickname = models.CharField(max_length=20)
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
#     votes = models.DecimalField(max_digits=10, decimal_places=0, default=0)
#     registered_at = models.DateTimeField(auto_now_add=True)
#     avatar = models.ImageField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     objects = MyUserManager()
#
#     # def __str__(self):
#     #     return self.username
#
#     def has_perm(self, perm, obj=None):
#         # "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         # "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         # "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
