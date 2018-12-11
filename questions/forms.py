from django import forms
from questions.models import *
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data['email'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count():
            raise forms.ValidationError('User with this email address is already exist')
        else:
            return self.cleaned_data['email']


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
        return obj
