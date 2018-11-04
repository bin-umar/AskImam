from django.shortcuts import render
from questions.models import Question, Answer
from datetime import timedelta, date
from django.core.paginator import Paginator


def list_questions(request, filter=None):
    questions = Question.objects.all()
    if filter is not None:
        today = date.today()
        if filter == 'news':
            questions = questions.order_by('-created_at')
        elif filter == 'hot':
            questions = questions.order_by('-votes', '-answer_count')
        elif filter == 'no_answer':
            questions = questions.filter(answer_count=0)
        elif filter == 'week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            questions = questions.filter(created_at__gte=start_week, created_at__lt=end_week)\
                .order_by('-votes', '-answer_count')
        elif filter == 'month':
            questions = questions.filter(created_at__month=today.month).order_by('-votes', '-answer_count')
        else:
            questions = questions.filter(tags__text__iexact=filter).order_by('-created_at')
    else:
        questions = questions.order_by('-created_at')

    paginator = Paginator(questions, 2)

    page = 1
    if 'page' in request.GET:
        _page = request.GET['page']
        if _page:
            page = _page

    questions = paginator.get_page(page)

    return render(request, "list_questions.html", {
        'questions': questions
    })


def login(request):
    return render(request, "logsup.html")


def sign_up(request):
    return render(request, "logsup.html")


def ask(request):
    return render(request, "ask.html")


def profile(request):
    return render(request, "profile.html")


def question(request, pk):
    one_question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question_id=pk)
    return render(request, "question.html", {
        'question': one_question,
        'answers': answers
    })
