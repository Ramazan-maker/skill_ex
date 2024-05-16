
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Feedback, ExchangeRequest, Skill, Course
from django.shortcuts import render

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SkillSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False)

def skill_search(request):
    form = SkillSearchForm(request.GET)
    skills = Skill.objects.all()

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        if keyword:
            skills = skills.filter(name__icontains=keyword)

    return render(request, 'skill_search.html', {'form': form, 'skills': skills})

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['sender', 'receiver', 'skill_offered', 'skill_requested']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text', 'rating']



class CourseForm(forms.ModelForm):
    title = forms.CharField(
        label='Название курса',
        validators=[RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слишком короткое название курса!'}
    )

    description = forms.CharField(label='Описание', widget=forms.Textarea)
    image = forms.ImageField(label='Изображение')  # Добавляем поле для изображения

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'Запрещенный курс':
            raise forms.ValidationError('К созданию не допускается!')
        return title

    class Meta:
        model = Course
        fields = ('title', 'description', 'image')