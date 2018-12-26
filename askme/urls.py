from django.contrib import admin
from django.urls import path, include
from questions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',              views.list_questions, name="index"),
    path('admin/',        admin.site.urls,      name="admin"),
    path('login/',        views.login,          name="login"),
    path('logout/',       views.logout,         name="logout"),
    path('signup/',       views.sign_up,        name="signUp"),
    path('ask/',          views.ask,            name="ask"),
    path('vote/',         views.vote,           name="vote"),
    path('profile/',      views.profile,        name="profile"),
    path('publish/',      views.publish,        name="publish"),
    path('getTokenCn/',   views.get_token,      name="get_token"),
    path('question/<int:pk>/', views.question,  name='question'),
    path('answer/<int:question_id>/', views.answer,       name='answer'),
    path('questions/<slug:filter>', views.list_questions, name="filteredIndex"),
    path('question/<int:q_id>/answer/<int:a_id>', views.set_answer_true,  name='set_answer_true'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
