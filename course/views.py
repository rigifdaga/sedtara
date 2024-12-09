from django.http import JsonResponse
from .models import Course, Module
from django.shortcuts import get_object_or_404

def get_all_courses(request):
    courses = Course.objects.select_related('teacher').order_by('-course_id')

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

def get_course_by_id(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)

    course_data = {
        'course_id': course.course_id,
        'course_name': course.course_name,
        'teacher_full_name': course.teacher.full_name,
        'course_description': course.course_description,
        'modules': []
    }

    modules = course.module_set.all().order_by('module_id')
    for module in modules:
        course_data['modules'].append({
            'module_id': module.module_id,
            'module_name': module.module_name
        })
    
    return JsonResponse(course_data)

def get_module_by_id(request, course_id, module_id):
    module = get_object_or_404(Module, module_id=module_id)

    module_data = {
        'module_id': module.module_id,
        'module_name': module.module_name,
        'materials': []
    }

    materials = module.materials_set.all().order_by('material_id')
    for material in materials:
        module_data['materials'].append({
            'material_id': material.material_id,
            'material_title': material.material_title,
            'material_attachment': material.material_attachment
        })
    
    return JsonResponse(module_data)