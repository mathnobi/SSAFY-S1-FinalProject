from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.conf import settings
from .models import DepositProducts, DepositOptions, SavingsProducts, SavingsOptions
from .serializers import  DepositProductsSerializer, DepositOptionsSerializer, SavingsProductsSerializer, SavingsOptionsSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()
    return Response(response)

@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()
    for item in response['result']['baseList']:
        fin_prdt_cd = item.get('fin_prdt_cd')
        kor_co_nm = item.get('kor_co_nm')
        fin_prdt_nm = item.get('fin_prdt_nm')
        join_way = item.get('join_way')
        etc_note = item.get('etc_note')
        join_deny = int(item.get('join_deny'))  # 정수형으로 변환
        join_member = item.get('join_member')
        spcl_cnd = item.get('spcl_cnd')

        # 중복 확인
        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm, fin_prdt_nm=fin_prdt_nm, join_way=join_way, etc_note=etc_note, join_deny=join_deny, join_member=join_member).exists():
            continue

        save_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'join_way':join_way,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'spcl_cnd':spcl_cnd
        }

        product_serializer = DepositProductsSerializer(data=save_data)
        if product_serializer.is_valid(raise_exception=True):
            product = product_serializer.save()
    
    for item in response['result']['optionList']:
        fin_prdt_cd = item.get('fin_prdt_cd')
        intr_rate_type_nm = item.get('intr_rate_type_nm')
        intr_rate = item.get('intr_rate')
        intr_rate2 = item.get('intr_rate2')
        save_trm = item.get('save_trm')
        
        deposit_product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        if DepositOptions.objects.filter(product=deposit_product.id, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2).exists():
            continue

        options_data = {
                'product': deposit_product.id,
                'fin_prdt_cd': deposit_product.fin_prdt_cd,
                'intr_rate_type_nm': item.get('intr_rate_type_nm'),
                'intr_rate': item.get('intr_rate')  if item.get('intr_rate') is not None else -1,
                'intr_rate2': item.get('intr_rate2')  if item.get('intr_rate2') is not None else -1,
                'save_trm': item.get('save_trm'), 
            }

        option_serializer = DepositOptionsSerializer(data=options_data)
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(product=deposit_product)

    return JsonResponse({ 'message': '저장 성공' })

@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        product = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(product, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pass



@api_view(['GET'])
def deposit_products_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    if options.exists():
        serializer = DepositOptionsSerializer(options, many=True)  # 여러 객체를 serializer에 전달
        return Response(serializer.data)

@api_view(['GET'])
def deposit_products_detail(request, fin_prdt_cd):
    product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def save_savings_products(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()
    for item in response['result']['baseList']:
        fin_prdt_cd = item.get('fin_prdt_cd')
        kor_co_nm = item.get('kor_co_nm')
        fin_prdt_nm = item.get('fin_prdt_nm')
        join_way = item.get('join_way')
        etc_note = item.get('etc_note')
        join_deny = int(item.get('join_deny'))  # 정수형으로 변환
        join_member = item.get('join_member')
        # spcl_cnd = item.get('spcl_cnd')

        # 중복 확인
        if SavingsProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm, fin_prdt_nm=fin_prdt_nm, join_way=join_way, etc_note=etc_note, join_deny=join_deny, join_member=join_member).exists():
            continue

        save_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'join_way':join_way,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            # 'spcl_cnd':spcl_cnd
        }

        product_serializer = SavingsProductsSerializer(data=save_data)
        if product_serializer.is_valid(raise_exception=True):
            product = product_serializer.save()
    
    for item in response['result']['optionList']:
        fin_prdt_cd = item.get('fin_prdt_cd')
        intr_rate_type_nm = item.get('intr_rate_type_nm')
        intr_rate = item.get('intr_rate')
        intr_rate2 = item.get('intr_rate2')
        save_trm = item.get('save_trm')
        
        savings_product = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        if SavingsOptions.objects.filter(product=savings_product.id, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2).exists():
            continue

        options_data = {
                'product': savings_product.id,
                'fin_prdt_cd': savings_product.fin_prdt_cd,
                'intr_rate_type_nm': item.get('intr_rate_type_nm'),
                'intr_rate': item.get('intr_rate')  if item.get('intr_rate') is not None else -1,
                'intr_rate2': item.get('intr_rate2')  if item.get('intr_rate2') is not None else -1,
                'save_trm': item.get('save_trm'), 
            }

        option_serializer = SavingsOptionsSerializer(data=options_data)
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(product=savings_product)

    return JsonResponse({ 'message': '저장 성공' })

@api_view(['GET', 'POST'])
def savings_products(request):
    if request.method == 'GET':
        product = get_list_or_404(SavingsProducts)
        serializer = SavingsProductsSerializer(product, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        serializer = SavingsProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pass

@api_view(['GET'])
def savings_products_options(request, fin_prdt_cd):
    options = SavingsOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    if options.exists():
        serializer = SavingsOptionsSerializer(options, many=True)  # 여러 객체를 serializer에 전달
        return Response(serializer.data)

@api_view(['GET'])
def savings_products_detail(request, fin_prdt_cd):
    product = get_object_or_404(SavingsProducts, fin_prdt_cd=fin_prdt_cd)
    serializer = SavingsProductsSerializer(product)
    return Response(serializer.data)
