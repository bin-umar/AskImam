from django.shortcuts import render, redirect, reverse
from questions.models import *
from django.core.paginator import Paginator
from questions.forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout as d_logout, login as d_login
from django.contrib.auth.decorators import login_required


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


def status_response(status, message):
    return JsonResponse({'status': status, 'message': message})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            try:
                user = User.objects.get(email__iexact=cdata['email'])
            except User.DoesNotExist:
                return status_response(False, {'email': 'User by this email not found!!'})
            else:
                user = authenticate(username=user.username, password=cdata['password'])
                if user is not None:
                    d_login(request, user)
                    next = request.POST.get('next', '/')
                    return status_response(True, next)
                else:
                    return status_response(False, {'login': 'Login or password is wrong!!'})
        else:
            return status_response(False, form.errors)
    
    return render(request, "logsup.html")


@login_required
def logout(request):
    d_logout(request)
    return redirect(reverse('index'))


def sign_up(request):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            d_login(request, user)
            return status_response(True, "/")
        else:
            return status_response(False, form.errors)

    return render(request, "logsup.html")


@login_required(login_url='/login/')
def ask(request):
    return render(request, "ask.html")


@login_required(login_url='/login/')
def profile(request):
    return render(request, "profile.html")


def question(request, pk):
    one_question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question_id=pk)
    return render(request, "question.html", {
        'question': one_question,
        'answers': answers
    })
