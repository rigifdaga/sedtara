import jwt
from django.conf import settings
from .models import Users
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt_token') or request.headers.get('Authorization')

        if token:
            try:
                if token.startswith("Bearer "):  # Jika token dikirim di Authorization header
                    token = token.split(" ")[1]

                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')

                user = Users.objects.filter(user_id=user_id).first()
                if user:
                    request.user = user
                else:
                    request.user = None
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
        else:
            request.user = None

        response = self.get_response(request)
        return response
