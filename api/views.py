from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from decimal import Decimal, InvalidOperation
from api.models import Order, Product
# Create your views here.

def health_check(request):
    return HttpResponse('Hello world')

ACCEPTED_TOKEN = ('omni_pretest_token')

def require_api_token(tokens):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return HttpResponseBadRequest('Missing or invalid Authorization header')

            token = auth_header.split(" ")[1]
            if token not in tokens :
                return HttpResponseBadRequest('Invalid Access Token')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@api_view(['POST'])
@require_api_token
def import_order(request):

    total_price = request.data.get('total_price')
    if total_price is None :        
        return JsonResponse(
            {"error": "total_price must be a valid decimal number"},
            status=400
        )

    try : 
        total_price = Decimal(total_price)

    except(InvalidOperation, TypeError) :
        return JsonResponse(
            {"error": "total_price must be a valid decimal number"},
            status=400
        )
    
    order = Order.objects.create(total_price=total_price)
    
    return JsonResponse({
        "message": "Order imported successfully",
        "order_number": order.order_number,
        "total_price": str(order.total_price),
        "created_time": order.created_time,
    }, status=200)

