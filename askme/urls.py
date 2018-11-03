"""
AskMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL-conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path, include
from questions import views

urlpatterns = [
    path('', views.list_questions, name="index"),
    path('admin/', admin.site.urls, name="admin"),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name="signUp"),
    path('ask/', views.ask, name="ask"),
    path('profile/', views.profile, name="profile"),
    path('question/<int:pk>/', views.question, name='question'),
    path('tinymce/', include('tinymce.urls')),
]




