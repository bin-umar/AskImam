from django.core.management.base import BaseCommand
from datetime import datetime
from faker import Faker
import random
from questions.models import *
from types import FunctionType
from functools import wraps

USER_COUNT = 100
TAG_COUNT = 100
QUESTION_COUNT = 250
ANSWER_COUNT = 500
VOTE_COUNT = 3000


def profile(obj):
    if isinstance(obj, FunctionType):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            _time_start = datetime.now()
            print("\'%s\' started" % obj.__qualname__)
            result = obj(*args, **kwargs)
            _time_stop = datetime.now()
            print("\'%s\' finished in %fs" % (obj.__qualname__, (_time_stop - _time_start).total_seconds()))
            return result
        return wrapper
    else:
        for attr_name in obj.__dict__:
            attr_body = getattr(obj, attr_name)
            if isinstance(attr_body, FunctionType):
                setattr(obj, attr_name, profile(attr_body))
        return obj


@profile
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_users()
        users = User.objects.all()

        self.create_tags()
        tags = Tag.objects.all()

        self.create_questions(users=users)
        questions = Question.objects.all()
        self.add_tag_question_relations(questions=questions, tags=tags)

        self.create_answers(questions=questions, users=users)
        # Нужно, т.к. при множественном добавлении не вызывается сигнал post_save
        self.count_answer_count(questions=questions)
        answers = Answer.objects.all()

        self.generate_likes_fast(users=users)

    def create_users(self):
        users = []
        faker = Faker()
        for i in range(USER_COUNT):
            user = User(username=faker.user_name()+str(i), password='passwd{}'.format(i), email=faker.email())
            users.append(user)

        User.objects.bulk_create(users, batch_size=10000)

    def create_tags(self):
        tags = []
        faker = Faker()
        for i in range(TAG_COUNT):
            tag = Tag(text=faker.word()+str(i))
            tags.append(tag)

        Tag.objects.bulk_create(tags, batch_size=10000)

    def create_questions(self, users):
        questions = []
        faker = Faker()
        for _ in range(QUESTION_COUNT):
            question = Question(title=faker.sentence()[:random.randint(20, 100)],
                                text=faker.text(),
                                author=random.choice(users))
            questions.append(question)

        Question.objects.bulk_create(questions, batch_size=10000)

    def create_answers(self, users, questions):
        answers = []
        faker = Faker()
        for _ in range(ANSWER_COUNT):
            answer = Answer(author=random.choice(users), question=random.choice(questions), text=faker.text(), is_true=False)
            answers.append(answer)

        Answer.objects.bulk_create(answers, batch_size=10000)

    def count_answer_count(self, questions):
        for question in questions:
            question.answer_count = question.answer_set.count()
        Question.bulk_objects.bulk_update(questions, update_fields=['answer_count'], batch_size=10000)

    def generate_likes_fast(self, users):

        Vote.objects.all().delete()

        questions = Question.objects.filter(pk__lte=10000)
        answers = Answer.objects.filter(pk__lte=10000)

        while(Vote.objects.all().count() < VOTE_COUNT):
            user = random.choice(users)
            votes = []

            _questions = questions.exclude(author=user)
            for question in _questions:
                value = random.choice([1, -1])
                vote = Vote(value=value, user=user, content_object=question)
                votes.append(vote)

            _answers = answers.exclude(author=user)
            for answer in _answers:
                value = random.choice([1, -1])
                vote = Vote(value=value, user=user, content_object=answer)
                votes.append(vote)

            Vote.objects.bulk_create(votes)
            for vote in votes:
                vote.content_object.rate += vote.value
                vote.content_object.save(update_fields=['rate'])

    def add_tag_question_relations(self, questions, tags):
        for question in questions:
            tags_for_questions = []
            for _ in range(random.randint(1, 5)):
                tag = random.choice(tags)
                if tag.pk not in tags_for_questions:
                    tags_for_questions.append(tag.pk)
            question.tags.add(*tags_for_questions)
