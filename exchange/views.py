from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm, UserLoginForm, SkillSearchForm, ExchangeRequestForm, CourseForm
from .forms import FeedbackForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from rest_framework import viewsets
from .models import Skill, ExchangeRequest, Course
from .serializers import SkillSerializer, ExchangeRequestSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ExchangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRequest.objects.all()
    serializer_class = ExchangeRequestSerializer


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Redirect to the home page after successful registration
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a specific URL after login if necessary
                # Example: return redirect('home') if 'home' is your home page URL name
                return redirect('/')  # Redirect to the root URL after successful login
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')

# class LoginView(LoginView):
# #     template_name = 'login.html'
# # # class LogoutView(LoginRequiredMixin,LogoutView):
# # #     template_name = 'logout.html'
# def logout_view(request):
#     # Логика, если требуется
#     return render(request, 'logout.html')
# class CustomLoginView(auth_views.LoginView):
#     template_name = 'login.html'
#
# class CustomLogoutView(auth_views.LogoutView):
#     next_page = reverse_lazy('logout.html')
def send_exchange_request(request):
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Редирект на главную страницу или на страницу с подтверждением
    else:
        form = ExchangeRequestForm()
    return render(request, 'send_exchange_request.html', {'form': form})


def send_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect('/')  # Редирект на главную страницу или на страницу с подтверждением
    else:
        form = FeedbackForm()
    return render(request, 'send_feedback.html', {'form': form})


def course_list(request):
    all_courses = Course.objects.all()
    paginator = Paginator(all_courses, 10)
    page_number = request.GET.get('page')
    try:
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'course_list.html', {'courses': courses})

# def create_course(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('course_list')  # Перенаправляем на страницу списка курсов после успешного создания
#     else:
#         form = CourseForm()
#     return render(request, 'create_course.html', {'form': form})
# class create_course(CreateView):
#     template_name = 'create_course.html'
#     form_class = CourseForm
#     success_url = reverse_lazy('exchange:course_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
class create_course(CreateView):
    template_name = 'create_course.html'
    form_class = CourseForm
    success_url = reverse_lazy('exchange:course_list')

    def form_valid(self, form):
        # Дополнительная логика, если форма валидна
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Передаем форму в контекст
        return context

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')

def skill_search(request):
    query = request.GET.get('q')
    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'skill_search.html', {'courses': courses})


@login_required
def profile(request):
    return render(request, 'profile.html')
