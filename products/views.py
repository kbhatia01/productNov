from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from django.core.cache import cache

import products
from products.ProductSerializer import ProductSerializer


# Create your views here.

class ProductPagination(PageNumberPagination):
    page_size = 2  # default is 2
    page_size_query_param = 'page_size'  # if you want to change default


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

    def get(self, request):
        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            cache_key = 'product:{}'.format(product_id)
            data = cache.get(cache_key)
            if data:
                return Response(data, status=status.HTTP_200_OK)
            try:
                product = Product.objects.get(id=product_id)
                data = ProductSerializer(product).data
                cache.set(cache_key, data)
                return Response(data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response('Product not found', status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: HW
#  Create order service that will take product ids,
#  CALL PRODUCT SERVICE GET THE AMOUNT,
#  CALL PAYMENT TO GENERATE PAYMENT LINK
#  RETURN BACK TO POSTMAN