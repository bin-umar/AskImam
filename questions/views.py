from django.shortcuts import render
from questions.models import Question, Answer
# Create your views here.
# from Faker import fake


def list_questions(request):
    questions = Question.objects.filter().order_by('-created_at')[:5]
    return render(request, "list_questions.html", {
        'questions': questions
    })


def examples(request):
    return render(request, "examples.html")


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
