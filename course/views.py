from django.http import JsonResponse
from .models import Course, Module
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json

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

@require_http_methods(["POST"])
def create_module(request, course_id):
    try:
        data = json.loads(request.body)

        module_name = data.get('module_name')

        if not course_id or not module_name:
            return JsonResponse({"error": "course_id and module_name are required"}, status=400)

        course = Course.objects.filter(course_id=course_id).first()
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)

        new_module = Module(course=course, module_name=module_name)
        new_module.save()

        module_data = {
            'module_id': new_module.module_id,
            'module_name': new_module.module_name,
            'course_id': new_module.course.course_id,
        }

        return JsonResponse(module_data, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["PUT"])
def update_module(request, course_id, module_id):
    try:
        data = json.loads(request.body)
        module_name = data.get('module_name')

        if not module_name:
            return JsonResponse({"error": "module_name is required"}, status=400)

        course = Course.objects.filter(course_id=course_id).first()
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)

        module = Module.objects.filter(course=course, module_id=module_id).first()
        if not module:
            return JsonResponse({"error": "Module not found"}, status=404)

        module.module_name = module_name
        module.save()

        module_data = {
            'module_id': module.module_id,
            'module_name': module.module_name,
            'course_id': module.course.course_id,
        }

        return JsonResponse(module_data, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["DELETE"])
def delete_module(request, course_id, module_id):
    try:
        course = Course.objects.filter(course_id=course_id).first()
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)

        module = Module.objects.filter(course=course, module_id=module_id).first()
        if not module:
            return JsonResponse({"error": "Module not found"}, status=404)

        module.delete()

        return JsonResponse({"message": "Module deleted successfully"}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)