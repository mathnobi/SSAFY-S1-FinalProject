from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.conf import settings

# Create your views here.
@api_view(['GET'])
def index(request):
    API_KEY_EXCHANGE = settings.API_KEY_EXCHANGE
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': API_KEY_EXCHANGE,
        'data': 'AP01',
    }
    response = requests.get(url, params=params, verify=False)
    return Response(response.json())