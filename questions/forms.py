from django import forms
from questions.models import *
from django.contrib.auth.forms import UserCreationForm
from tinymce.models import HTMLField


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
    title = forms.CharField(required=True, min_length=8)
    text = HTMLField()
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author

        if commit:
            obj.save()

        tags_for_question = str(args[0]).split(',')
        tags = []

        for tag in tags_for_question:
            tag = tag.strip()
            try:
                _tag = Tag.objects.get(text__iexact=tag)
            except Tag.DoesNotExist:
                _tag = Tag(text=tag)
                _tag.save()
                tags.append(_tag.pk)
            else:
                tags.append(_tag.pk)

        obj.tags.add(*tags)
        return obj


class AnswerForm(forms.ModelForm):
    text = HTMLField()

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        obj.question = args[0]
        if commit:
            obj.save()

        return obj


class VoteForm(forms.ModelForm):
    obj_name = forms.CharField(required=True, max_length=8)
    obj_id = forms.IntegerField(required=True)
    value = forms.IntegerField(required=True)

    class Meta:
        model = Vote
        fields = ['value']

    def __init__(self, author, *args, **kwargs):
        self.user = author
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        obj_name = cleaned_data.get('obj_name')
        obj_id = cleaned_data.get('obj_id')
        value = cleaned_data.get('value')

        if obj_name != 'answer' and obj_name != 'question':
            self.add_error('obj_name', 'Wrong parameters')

        if value != 1 and value != -1:
            self.add_error('value', 'Vote value can be only 1 or -1')

        votes = Vote.objects.filter(user=self.user)\
                            .filter(content_type__model__iexact=obj_name)
        if votes:
            _votes = votes.filter(object_id=obj_id)
            _votes.exclude(value=value).delete()
            if _votes:
                self.add_error('value', 'Sorry but you have already voted!!!')

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        obj.content_object = args[0]
        obj.content_object.rate += obj.value
        obj.content_object.save(update_fields=['rate'])

        if commit:
            obj.save()
