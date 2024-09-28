from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if isinstance(response.data, dict) and "token_not_valid" in response.data.get("code", ""):
            return Response({"message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    return response
