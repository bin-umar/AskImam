from django.contrib import admin
from django.urls import path, include
from questions import views

urlpatterns = [
    path('',              views.list_questions, name="index"),
    path('<slug:filter>', views.list_questions, name="filteredIndex"),
    path('admin/',        admin.site.urls,      name="admin"),
    path('login/',        views.login,          name="login"),
    path('logout/',       views.logout,         name="logout"),
    path('signup/',       views.sign_up,        name="signUp"),
    path('ask/',          views.ask,            name="ask"),
    path('profile/',      views.profile,        name="profile"),
    path('question/<int:pk>/', views.question,  name='question'),
    path('tinymce/', include('tinymce.urls')),
]
