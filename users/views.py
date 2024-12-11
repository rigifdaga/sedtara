from django.conf import settings
from django.http import JsonResponse
from .models import Users
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
import json
import jwt
from datetime import datetime, timedelta, timezone

@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)

        username = data.get('username')
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)
        
        if not re.match(r'^[\w]+$', username):
            return JsonResponse({"error": "Username must be alphanumeric and can only contain underscores."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format."}, status=400)

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            return JsonResponse({"error": "Password must be at least 8 characters long and contain a letter, a number, an uppercase letter, a lowercase letter, and a symbol."}, status=400)

        if Users.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if Users.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = Users(
            username=username,
            email=email,
            full_name=full_name,
            password=make_password(password)
        )
        user.save()

        token = generate_jwt_token(user)

        response = JsonResponse({"message": "User registered successfully", "token": token})
        response.set_cookie(
            'jwt_token', token,
            max_age=timedelta(days=1),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response 

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def generate_jwt_token(user):
    now = datetime.now(timezone.utc)

    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'exp': now + timedelta(hours=24),
        'iat': now,
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"error": "username and password are required"}, status=400)

        user = Users.objects.filter(username=username).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        if check_password(password, user.password):
            token = generate_jwt_token(user)

            response = JsonResponse({"message": "User logged in successfully", "token": token})
            response.set_cookie(
                'jwt_token', token,
                max_age=timedelta(days=1),
                httponly=True,
                secure=True,
                samesite='Lax'
            )

            return response 
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["POST"])
def logout(request):
    response = JsonResponse({"message": "Logged out successfully"})
    response.delete_cookie('jwt_token')
    return response