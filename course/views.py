from django.http import JsonResponse
from .models import Course

def get_all_courses(request):
    courses = Course.objects.select_related('teacher').all()

    course_data = []
    for course in courses:
        course_data.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'teacher_full_name': course.teacher.full_name,
            'course_image': course.course_image,
            'course_description': course.course_description
        })

    return JsonResponse(course_data, safe=False)
