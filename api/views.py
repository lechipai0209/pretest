from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from decimal import Decimal, InvalidOperation
from api.models import Order
# Create your views here.

def health_check(request):
    return HttpResponse('Hello world')

ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    # Add your code here
    return HttpResponseBadRequest()