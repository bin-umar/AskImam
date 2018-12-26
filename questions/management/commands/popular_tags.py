from django.core.management.base import BaseCommand
from questions.models import Question, Answer
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.cache import cache


class Command(BaseCommand):

    def handle(self, *args, **options):
        last_three_months = datetime.today() - timedelta(days=90)
        questions = Question.objects.filter(created_at__gte=last_three_months)
        answers = Answer.objects.filter(created_at__gte=last_three_months)

        self.popular_tags(questions)
        self.popular_users(questions, answers)

    def popular_tags(self, questions):
        count = {}
        for question in questions:
            for tag in question.tags.all():
                if tag.pk in count:
                    count[tag.pk] += 1
                else:
                    count[tag.pk] = 1

        for c in count:
            print(str(c) + ': ' + str(count[c]))

        cache_key = 'popular_tags'
        cache_time = 3600  # time to live in seconds


    def popular_users(self, questions, answers):
        users = {}
        for question in questions:
            user = question.author
            if user.pk in users:
                users[user.pk] += 1
            else:
                users[user.pk] = 1

        for answer in answers:
            user = answer.author
            if user.pk in users:
                users[user.pk] += 1
            else:
                users[user.pk] = 1

        for u in users:
            print(str(u) + ': ' + str(users[u]))
