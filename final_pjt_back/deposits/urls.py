from django.urls import path
from . import views

app_name = 'deposits'
urlpatterns = [
    # 예금 상품 데이터 받아오는 주소
    path('', views.index, name="index"),
    path('save-deposit-products/', views.save_deposit_products, name="save_deposit_products"),
    path('deposit-products/', views.deposit_products, name="deposit_products"),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_products_options, name="deposit_products_options"),
    path('deposit-products/<str:fin_prdt_cd>/', views.deposit_products_detail, name="deposit_products_detail"),
    # 적금 상품 데이터 받아오는 주소
    path('save-savings-products/', views.save_savings_products, name="save_savings_products"),
    path('savings-products/', views.savings_products, name="savings_products"),
    path('savings-products-options/<str:fin_prdt_cd>/', views.savings_products_options, name="savings_products_options"),
    path('savings-products/<str:fin_prdt_cd>/', views.savings_products_detail, name="savings_products_detail"),
]
