from django.shortcuts import render
from questions.models import Question
from django.contrib.auth.models import User
from questions.models import Tag
from django.template.defaultfilters import slugify

# Create your views here.
# from Faker import fake

def listQuestions(request):
    questions = [
        {
            'title': 'We don’t know why you we got divorced...',
            'text': 'Salaam I got divorced last year from my husband and both of us did not know why. He came back to me ...',
            'created_at': '30.10.2018 20:13',
            'author': '',
            'votes': 500,
            'tags': ['Marriage', 'Divorce']
        },
        {
            'title': 'Foster Siblings Living Together',
            'text': 'Can foster brother and sister live togather in a same house?',
            'created_at': '28.10.2018 20:13',
            'votes': 23,
            'author': '',
            'tags': ['Misc', 'Fiqh']
        },
        {
            'title': 'Is whey protein concentrate Ḥalal?',
            'text': 'Is whey protein concentrate Ḥalal?',
            'created_at': '27.10.2018 20:13',
            'votes': 125,
            'author': '',
            'tags': ['Food', 'Drink']
        },
        {
            'title': 'My question is regarding the naming of a baby?',
            'text': 'My question is regarding the naming of a baby. We are due to welcome our baby in a couple of weeks.',
            'created_at': '27.10.2018 20:13',
            'votes': 61,
            'author': '',
            'tags': ['Child Upbringing (Tarbiyyah)']
        },
        {
            'title': 'Do Junaid Jamshed’s Anasheed contain Shirk?',
            'text': 'There is famous naat of Junaid Jamshed "Mai Toh Ummati Hu" and we knows he is ex-singer who use to '
                    'be a popstar but he ...',
            'created_at': '26.10.2018 20:13',
            'votes': 16,
            'author': '',
            'tags': ['Beliefs and Practices (Aqeedah)']
        }
    ]
    return render(request, "list_questions.html", {
        'questions': questions
    })

def examples(request):
    return render(request, "examples.html")

def login(request):
    return render(request, "logsup.html")

def signUp(request):
    return render(request, "logsup.html")

def ask(request):
    return render(request, "ask.html")

def profile(request):
    return render(request, "profile.html")

def question(request):
    # user = User.objects.create_user('johnson', 'lennon@thebeatles.com', 'johnpassword')
    question = Question(
        [Tag.objects.get(pk=1)],
        "Do Junaid Jamshed’s Anasheed contain Shirk?",
        "As salamo alaikum, Mufti Sahab, I am Zaid from Mumbai (Bombay), India and I really have a serious questions "
        "which is about issue of akhirah and kufr, shirk and my questions is 4, this will be really lengthy questions "
        "but not bigger than the knowledge of the alim or ulama like you, Alhumdurillah, but I beg u plzz give all the "
        "answers of all 4 questions in detail and in depth as it's about matter of someone's akhirah and I really wanna"
        " know all this it's a big request, the following Questions are: "
        "<br> <br> Question No.1 - There is famous naat of Junaid "
        " Jamshed 'Mai Toh Ummati Hu' and we knows he is ex-singer who use to be a popstar but he gave up music later "
        " on and joined Tablighi Jamat and he was a Deobandi of Tablighi Jamat who died few years ago in plane crash in "
        "tablighi mission and peoples even called him shaheed (martyr) and he is inspired by Maulana Tariq Jameel, but"
        " I found the lyrics to be Shirkiya (Polythiestic) and here are the some verses Mai Toh Ummati Hoon Aye Shah e Umam "
        "<br><br> Karden Mere Aaqa Ab Nazr e Karam    "
        "<br> Mai Toh Be Sahara Hoon Daman Bhi Hai Khali "
        "<br> Nabiyon Ke Nabi Teri Shan Hai Nirali "
        "<br> Gham Ke Andheron Ne Ghera Hua Hai "
        "<br> Aaqa Dushwar Ab Jeena Mera Hua Hai "
        "<br> Bigri Bana Do Meri Aye Taiba Ke Wali "
        "<br> Nabiyon Ke Nabi Teri Shan Hai Nirali?????? "
        "<br><br> Bigri Bana Do Meri Taiba Aaye Taiba Ke Wali doesn't look clear shirk? As Rasul Allah is not here neither he "
        "is omnipresent but he is calling him in naat???? And I saw in video that he sang this naat in front of Maulana"
        " Tariq Jameel also and Maulana Tariq Jameel is biggest Tablighi/Deobandi Preacher of Pakistan in the modern"
        " era, he didn't even stop him but rather he was listening along with more other peoples, furthermore there is"
        " also another naat which looks even more clear shirk and Junaid Jamshed sang this naat before death in the news"
        " channel which was in the memory of sabri brothers (one of the qawali group in pakistan) and the lyrics is"
        " 'Bhar De Jholi Meri Ya MohammadLautkar Main Naa Jaunga Khaali...there is also further but I didn't heard from"
        " Junaid Jamshed i.e Jab Talak Tu Bana De Na Tu Bigdi Dar Se Tere Na Jaaye Sawali (this is also took as a"
        " Bollywood song in the Bollywood film of Salman Khan, Bajrangi Bhaijan), I am really tensed that Junaid Jamshed"
        " is mushrik and if yes so what about those who called him shaheed?? And also Maulana Tariq Jameel will be in"
        " same category who didn't stopped him???? kindly answer in detail plzzz",
        "26.10.2018 20:13",
        User.objects.get(pk=1),
        16
    )

    return render(request, "question.html", {
        'question': question
    })

def new_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, "list_questions.html", {
        'questions': questions
    })

# def question(request, pk):
#     question = Question.objects.get(pk=pk)
#     return render(request, "question.html", {
#         'question': question
#     })



