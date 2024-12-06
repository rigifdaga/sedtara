from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Scholarship

# GET semua data atau filter berdasarkan education_level atau search
def get_all_scholarships(request):
    education_level = request.GET.get('education_level', None)
    query = request.GET.get('query', None)
    
    scholarships = Scholarship.objects.all()

    if education_level:
        scholarships = scholarships.filter(education_level=education_level)

    if query:
        scholarships = scholarships.filter(
            Q(scholarship_name__icontains=query) |
            Q(description__icontains=query) |
            Q(provider__icontains=query)
        )

    return JsonResponse(list(scholarships.values()), safe=False)

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
