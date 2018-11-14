from django import forms
from questions.models import Question


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


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
