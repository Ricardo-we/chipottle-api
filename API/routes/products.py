from API.models import Admins, Products
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from API.serializers import ProductsSerializer
from django.core.paginator import Paginator

def get_products(request):
    if(request.GET.get('limit') and request.GET.get('page')): 
        limit = request.GET.get('limit')
        page = request.GET.get('page')
        
        all_products = Products.objects.all()
        products = list(all_products.values())
        for i in range(len(all_products)):
            products[i]['item_image'] = all_products[i].item_image.url
        paginator = Paginator(products, limit)
        data = {
            'last_page': paginator.num_pages,
            'has_previous': paginator.page(page).has_previous(),
            'has_next':paginator.page(page).has_next(),
            'products':paginator.page(page).object_list,
        }
        return JsonResponse(data, safe=False)

    elif(request.GET.get('product-id')): 
        products = Products.objects.filter(id=request.GET.get('product-id'))
        product = list(products.values())[0]
        product['item_image'] = products[0].item_image.url
        return JsonResponse(product, safe=False)

    all_products = Products.objects.all()
    products = list(all_products.values())
    for i in range(len(all_products)):
        products[i]['item_image'] = all_products[i].item_image.url
    return JsonResponse(products, safe=False)    

def create_product(request):
    item_name = request.data.get('product-name')
    item_price =  request.data.get('product-price')
    item_description =  request.data.get('product-description')
    item_image = request.FILES.get('product-image')
    
    product = Products(item_name=item_name, item_price=item_price, item_image=item_image, item_description=item_description)
    product.save()

    return JsonResponse({'message': 'Product added successfully'}, safe=False)

def delete_product(pk):
    try:
        Products.objects.filter(pk=pk).delete()
        return JsonResponse({'message': 'Product deleted successfully'}, safe=False)
    except:
        return JsonResponse({'message': 'Product deleted successfully'}, safe=False)

def update_product(request, pk):
    product = Products.objects.get(id=pk)
    product.item_name = request.data.get('product-name')
    product.item_price =  request.data.get('product-price')
    product.item_description =  request.data.get('product-description')
    if(request.FILES.get('product-image')): product.item_image = request.FILES.get('product-image')
    product.save()
    return JsonResponse({'message': 'Product updated successfully'}, safe=False)


@csrf_exempt
@api_view(['POST', 'PUT', 'DELETE', 'GET'])
@parser_classes([MultiPartParser])
def manage_products(request, pk=''):
    key = request.data.get('key')
    # try:
    if(request.method == 'GET'):
        return get_products(request)
    if(Admins.objects.get(admin_key=key)):
        if(request.method == 'POST'):
            return create_product(request)
        elif(request.method == 'PUT'):
            return update_product(request, pk)
        elif(request.method == 'DELETE'):
            return delete_product(pk)
        return JsonResponse({'message': 'Invalid key'}, safe=False)
# except:
    # return JsonResponse({'message': 'Something went wrong, or invalid input'}, safe=False)
    return JsonResponse({'message': 'No input or invalid'}, safe=False)
