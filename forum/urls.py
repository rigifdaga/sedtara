from django.urls import path
from . import views

urlpatterns = [
    path('questions/create/', views.create_question, name='create_question'),
]
