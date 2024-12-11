from django.urls import path
from .views import get_all_courses, get_course_by_id, get_module_by_id, create_module, update_module, delete_module

urlpatterns = [
    path('course/', get_all_courses, name='get_all_courses'),
    path('course/<int:course_id>/', get_course_by_id, name='get_course_by_id'),
    path('course/<int:course_id>/module', create_module, name='get_course_by_id'),
    path('course/<int:course_id>/<int:module_id>/delete', delete_module, name='delete_module'),
    path('course/<int:course_id>/<int:module_id>/update', update_module, name='update_module'),
    path('course/<int:course_id>/<int:module_id>/read', get_module_by_id, name='get_module_by_id'),
]