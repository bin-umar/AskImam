from django.shortcuts import render, redirect, reverse
from questions.models import Question, Answer
from django.core.paginator import Paginator
from questions.forms import LoginForm
from django.contrib import auth


def pager(request, iterable):
    paginator = Paginator(iterable, 10)

    page = 1
    if 'page' in request.GET:
        _page = request.GET['page']
        if _page:
            page = _page

    return paginator.get_page(page)


def list_questions(request, filter=None):
    if filter is not None:
        if filter == 'news':
            questions = Question.objects.news()
        elif filter == 'hot':
            questions = Question.objects.hot()
        elif filter == 'no_answer':
            questions = Question.objects.no_answer()
        elif filter == 'week':
            questions = Question.objects.week()
        elif filter == 'month':
            questions = Question.objects.month()
        else:
            questions = Question.objects.by_tag(filter)
    else:
        questions = Question.objects.news()

    questions = pager(request, questions)

    return render(request, "list_questions.html", {
        'questions': questions
    })


def login(request):
    return render(request, "logsup.html")


def logout(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate()
    return redirect(reverse('index'))


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
