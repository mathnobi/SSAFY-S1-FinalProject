from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserDetailsSerializer

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = CustomUserDetailsSerializer(request.user)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserDetailsSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
