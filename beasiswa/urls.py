from django.urls import path
from .views import get_scholarships

urlpatterns = [
    path('scholarships/', get_scholarships, name='get_scholarships'),
    path('scholarships/<int:id>/', get_scholarships, name='get_scholarship_by_id'),
]