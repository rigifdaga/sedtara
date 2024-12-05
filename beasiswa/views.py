from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Scholarship

# GET semua data atau filter berdasarkan education_level
def get_all_scholarships(request):
    education_level = request.GET.get('education_level', None)
    if education_level:
        scholarships = Scholarship.objects.filter(education_level=education_level).values()
    else:
        scholarships = Scholarship.objects.all().values()
    return JsonResponse(list(scholarships), safe=False)

# GET berdasarkan ID
def get_scholarship_by_id(request, id):
    scholarship = get_object_or_404(Scholarship, pk=id)
    return JsonResponse({
        "scholarship_id": scholarship.scholarship_id,
        "education_level": scholarship.education_level,
        "scholarship_name": scholarship.scholarship_name,
        "description": scholarship.description,
        "end_date": scholarship.end_date,
        "provider": scholarship.provider,
        "benefit": scholarship.benefit,
        "link": scholarship.link,
    })
