from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import Product

import products
from products.ProductSerializer import ProductSerializer


# Create your views here.

class ProductPagination(PageNumberPagination):
    page_size = 2  # defualt is 2
    page_size_query_param = 'page_size'  #if you want to change default


class ProductViewSet(APIView):
    def post(self, request, format=None):
        page_size = request.data.get('page_size', 2)
        ordering = request.data.get('ordering', '-created_at')
        querys = request.data.get('query')
        query = Product.objects.filter(name__icontains=querys).order_by(ordering)

        # pagination..
        paginator = ProductPagination()
        paginator.page_size = page_size
        paginated_query = paginator.paginate_queryset(query, request)

        serializer = ProductSerializer(paginated_query, many=True)

        return paginator.get_paginated_response(serializer.data)
