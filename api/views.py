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


# clients make orders
@api_view(['POST'])
@require_api_token([ACCEPTED_TOKEN, SUPERUSER_TOKEN])
def import_order(request):

    product_id = request.data.get('product_id')
    product_amount = request.data.get('product_amount')

    if not product_id:
        return JsonResponse({"error": "product_id is required"}, status=400)

    try:
        product_id = int(product_id)
        if product_id <= 0:
            return JsonResponse({"error": "product_id must be a positive integer"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "product_id must be an integer"}, status=400)
    
    try:
        product_amount = int(product_amount)
        if product_amount <= 0:
            return JsonResponse({"error": "product_amount must be greater than 0"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "product_amount must be an integer"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=400)

    total_price = product.price * product_amount

    order = Order.objects.create(
        product=product,
        product_amount=product_amount,
        total_price=total_price
    )

    return JsonResponse({
        "message": "Order imported successfully",
        "order_number": order.order_number,
        "product_id": product.id,
        "product_name": product.name,
        "product_amount": order.product_amount,
        "total_price": order.total_price,
        "created_time": order.created_time,
    }, status=200)



# superuser add products
@api_view(['POST'])
@require_api_token([SUPERUSER_TOKEN])
def import_product(request):
    name = request.data.get('name')
    price = request.data.get('price')

    if not name or not name.strip():
        return JsonResponse({"error": "Product name is required"}, status=400)

    try:
        price = Decimal(price)
        if price <= 0:
            return JsonResponse({"error": "Price must be greater than 0"}, status=400)
    except (InvalidOperation, TypeError):
        return JsonResponse({"error": "Invalid price value"}, status=400)

    product = Product.objects.create(name=name.strip(), price=price)

    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "price": str(product.price)
    }, status=200)

# clients get all products
@api_view(['GET'])
@require_api_token([ACCEPTED_TOKEN, SUPERUSER_TOKEN])
def get_products(request):

    products = Product.objects.all()
    return JsonResponse([{
        "id": product.id,
        "name": product.name,
        "price": str(product.price)
    } for product in products], safe=False)

@api_view(['GET'])
@require_api_token([SUPERUSER_TOKEN])
def get_orders(request):
    orders = Order.objects.all()
    return JsonResponse([{
        "order_number": order.order_number,
        "product_id": order.product.id,
        "product_name": order.product.name,
        "product_amount": order.product_amount,
        "total_price": order.total_price,
        "created_time": order.created_time,
    } for order in orders], safe=False)
