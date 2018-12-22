from django.shortcuts import render, redirect, reverse
from questions.models import *
from django.core.paginator import Paginator
from questions.forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout as d_logout, login as d_login
from django.contrib.auth.decorators import login_required
from urllib import parse


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

    return render(request, 'list_questions.html', {
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

    next = parse.urlparse(request.META.get('HTTP_REFERER')).path
    return render(request, 'login.html', {'next': next})


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
            return status_response(True, '/')
        else:
            return status_response(False, form.errors)

    return render(request, 'signup.html')


@login_required(login_url='/login/')
def ask(request):
    if request.POST:
        form = QuestionsForm(request.user, request.POST)
        if form.is_valid():
            question = form.save(request.POST.get('tags'))
            return status_response(True, '/question/' + str(question.pk))
        else:
            return status_response(False, form.errors)

    return render(request, 'ask.html')


@login_required(login_url='/login/')
def answer(request, question_id):
    if request.POST:
        form = AnswerForm(request.user, request.POST)
        if form.is_valid():
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return redirect(reverse('index'))
            else:
                answer = form.save(question)
            return redirect(reverse('question', kwargs={'pk': question.pk}) + '#answer_' + str(answer.pk))
        else:
            return redirect('/question/' + str(question_id)) #It should be replaced with error page


@login_required(login_url='/login/')
def profile(request):
    profile = Profile.objects.get(user_id__exact=request.user.pk)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html', {'user': profile.user})
        else:
            print(form.errors)
            return render(request, 'profile.html', {
                        'user': profile.user,
                        'errors': form.errors
                        })
    return render(request, 'profile.html')


def question(request, pk):
    one_question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question_id=pk)
    one_is_true = answers.filter(is_true=True).count() >= 1

    user_id = 0
    if request.user:
        user_id = request.user.pk

    return render(request, 'question.html', {
        'question': one_question,
        'one_is_true': one_is_true,
        'user_id': user_id,
        'answers': answers
    })


@login_required(login_url='/login/')
def vote(request):
    if request.POST:
        form = VoteForm(request.user, request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            if cdata['obj_name'] == 'answer':
                try:
                    answer = Answer.objects.get(pk=cdata['obj_id'])
                except Answer.DoesNotExist:
                    return status_response(False, {'answer': 'Answer by this doesn\'t exist'})
                else:
                    form.save(answer)
            else:
                try:
                    question = Question.objects.get(pk=cdata['obj_id'])
                except Question.DoesNotExist:
                    return status_response(False, {'question': 'Question by this doesn\'t exist'})
                else:
                    form.save(question)

            return status_response(True, 'Vote successfully added')
        else:
            return status_response(False, form.errors)


@login_required(login_url='/login/')
def set_answer_true(request, q_id, a_id):
    try:
        question = Question.objects.get(pk=q_id)
    except Question.DoesNotExist:
        return status_response(False, 'Couldn\'t find question by this id')
    else:
        try:
            answer = Answer.objects.get(pk=a_id)
        except Answer.DoesNotExist:
            return status_response(False, 'Couldn\'t find answer by this id')
        else:
            if request.user.pk == question.author_id:
                is_true = request.POST.get('is_true', False)
                if is_true == 'true':
                    is_true = True
                elif is_true == 'false':
                    is_true = False
                answer.is_true = is_true
                answer.save()
            else:
                return status_response(False, 'Sorry but its not your question!!')

    return status_response(True, 'Successfully')
