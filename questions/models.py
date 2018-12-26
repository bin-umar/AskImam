from django.shortcuts import reverse
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_bulk_update.manager import BulkUpdateManager
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .managers import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='avatars/default-avatar.png')


class Vote(models.Model):
    VOTES = (
        (1, 'Like'),
        (-1, 'Dislike')
    )

    value = models.SmallIntegerField(default=VOTES[0], choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        indexes = [
            models.Index(fields=['content_type']),
        ]


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_count = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    votes = GenericRelation(Vote, related_query_name='questions')
    rate = models.IntegerField(default=0)
    tags = models.ManyToManyField(to='Tag', related_name='questions')

    objects = QuestionsManager()
    bulk_objects = BulkUpdateManager()

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})


class Tag(models.Model):
    text = models.SlugField(unique=True)


class Answer(models.Model):
    text = HTMLField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    record_date = models.DateTimeField(auto_now_add=True)
    is_true = models.BooleanField(default=False)
    votes = GenericRelation(Vote, related_query_name='answers', default=0)
    rate = models.IntegerField(default=0)


@receiver(post_save, sender=Answer)
def inc_question_answer_count(sender, instance, created, **kwargs):
    if created:
        instance.question.answer_count += 1
        instance.question.save()


@receiver(post_delete, sender=Answer)
def dec_question_answer_count(sender, instance, **kwargs):
    instance.question.answer_count -= 1
    instance.question.save()
