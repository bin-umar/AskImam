from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.DecimalField(max_digits=5, decimal_places=4)
    tags = models.ManyToManyField(to='Tag', related_name='questions')

    # def __init__(self, _title, _text, _created_at, _author, _votes, _tags):
    #     self.title = _title
    #     self.text = _text
    #     self.created_at = _created_at
    #     self.author = _author
    #     self.votes = _votes
    #     self.tags = _tags

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})

class Tag(models.Model):
    text = models.SlugField(unique=True)


