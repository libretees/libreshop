from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .models import Product

# Create your views here.
def home_page(request):
    products = Product.objects.all()
    return render_to_response('shop/home.html', {'products': products})

def product_page(request):
    return render(request, 'shop/product.html')
