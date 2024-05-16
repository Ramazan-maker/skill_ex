from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'exchange'

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'exchanges', ExchangeRequestViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('', index, name='home'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('logout/', views.logout_view, name='logout'),

    path('profile/', profile, name='profile'),
    path('skill_search/', skill_search, name='skill_search'),
    path('send_exchange_request/', send_exchange_request, name='send_exchange_request'),
    path('send_feedback/', send_feedback, name='send_feedback'),
    path('create_course/', create_course.as_view(), name='create_course'),  # Use CreateCourse as a class-based view
    path('course_list/', course_list, name='course_list'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    # path('', redirect_to_index),
]

