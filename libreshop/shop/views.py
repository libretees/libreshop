from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .models import Product

# Create your views here.
def home_page(request):
    return render(request, 'shop/home.html')

def product_page(request):
    return render(request, 'shop/product.html')
