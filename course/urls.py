from django.urls import path
from .views import get_all_courses

urlpatterns = [
    path('course/', get_all_courses, name='get_all_courses'),
]