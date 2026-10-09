"""CORS mínimo para desarrollo local. En producción, limita orígenes explícitamente."""
from django.conf import settings

class LocalDevelopmentCorsMiddleware:
    allowed_origins = {"http://localhost:5173", "http://127.0.0.1:5173"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        if request.method == "OPTIONS" and origin in self.allowed_origins:
            from django.http import HttpResponse
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)
        if origin in self.allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Vary"] = "Origin"
        return response
