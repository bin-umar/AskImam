from django.db import models
from datetime import timedelta, date


class QuestionsManager(models.Manager):
    def news(self):
        return self.all().order_by('-created_at')

    def hot(self):
        return self.all().order_by('-rate')

    def no_answer(self):
        return self.filter(answer_count=0)

    def week(self):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        return self.filter(created_at__gte=start_week, created_at__lt=end_week)\
            .order_by('-rate', '-answer_count')

    def month(self):
        today = date.today()
        return self.filter(created_at__month=today.month).order_by('-rate', '-answer_count')

    def by_tag(self, tag):
        return self.filter(tags__text__iexact=tag).order_by('-created_at')
