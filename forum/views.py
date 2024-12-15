from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Questions, Answers
from datetime import datetime
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_question(request):
    if not request.user:  # Periksa apakah user sudah login
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        data = json.loads(request.body)

        new_question = Questions.objects.create(
            question=data.get('question'),
            category=data.get('category'),
            created_at=datetime.now(),
            asker=request.user
        )

        return JsonResponse({
            "message": "Question created successfully",
            "question_id": new_question.question_id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
