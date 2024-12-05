from django.urls import path
from .views import get_all_scholarships, get_scholarship_by_id

urlpatterns = [
    path('scholarships/', get_all_scholarships, name='get_all_scholarships'),
    path('scholarships/<int:id>/', get_scholarship_by_id, name='get_scholarship_by_id'),
]
