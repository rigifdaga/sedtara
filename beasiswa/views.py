from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Scholarship

def get_scholarships(request, id=None):
    if id:
        scholarship = get_object_or_404(Scholarship, pk=id)
        return JsonResponse({
            "scholarship_id": scholarship.scholarship_id,
            "education_level": scholarship.education_level,
            "scholarship_name": scholarship.scholarship_name,
            "description": scholarship.description,
            "end_date": scholarship.end_date,
            "provider": scholarship.provider,
            "benefit": scholarship.benefit,
        })
    else:
        scholarships = Scholarship.objects.all().values()
        return JsonResponse(list(scholarships), safe=False)
