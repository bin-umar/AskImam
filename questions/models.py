from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    votes = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    avatar = models.ImageField()


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
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
    text = HTMLField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=0)
    record_date = models.DateTimeField(auto_now_add=True)
    is_true = models.BooleanField()
    votes = models.DecimalField(max_digits=10, decimal_places=0, default=0)
