from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.conf import settings

# 완성 못한 부분
# 바로 vue에서 하는 방법들 보이는데 어떻게 하는게 좋을까?
# Create your views here.
@api_view(['GET'])
def index(request):
    API_KEY_BANKMAP = settings.API_KEY_BANKMAP

    params = {
        'authkey': API_KEY_BANKMAP,
    }
    return render(request, 'bankmap/index.html')