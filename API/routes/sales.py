from API.models import Products, Sales, Admins
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from API.utils import get_total_sales, get_totals

def get_sales():
    total_sales = get_total_sales()
    return JsonResponse({'total_sales': total_sales}, safe=False)

def get_sold_products():
    sales = list(Sales.objects.all().values())
    for sale in sales:
        sale['product'] = Products.objects.get(id=sale['sold_product_id']).item_name
        sale['product_price'] = Products.objects.get(id=sale['sold_product_id']).item_price

    return JsonResponse(sales, safe=False)

def get_sales_by_product(request):
    total_sales = get_totals(request.data.get('product-name'))
    return JsonResponse({'total_product_sales': total_sales},safe=False)

def add_sale(product_id):
    selled_product = Products.objects.get(id=product_id)
    sale = Sales(sold_product=selled_product)
    sale.save()
    return JsonResponse({'message': 'Sale added'}, safe=False)

def delete_sale(pk):
    Sales.objects.filter(id=pk).delete()
    return JsonResponse({'message': 'Sale deleted'})

def delete_sales_by_product(product_id):
    product = Products.objects.get(id=product_id)
    Sales.objects.filter(sold_product=product).delete()
    return JsonResponse({'message': f'Sales of {product.item_name} deleted'}, safe=False)

@csrf_exempt
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def manage_sales(request, pk=''):
    key = request.data.get('key')
    try:
        if(Admins.objects.filter(admin_key=key).exists()):
            if(request.method == 'POST' and request.GET.get('totals')):
                return get_sales()
            elif(request.method == 'POST' and request.GET.get('sold-products')):
                return get_sold_products()
            elif(request.method == 'DELETE' and request.data.get('delete-multiple')):
                return delete_sales_by_product(pk)
            elif(request.method == 'DELETE'):
                return delete_sale(pk)
        if(request.method == 'POST'):
            return add_sale(pk)

    except:
        return JsonResponse({'message': 'Something went wrong, or invalid input'}, safe=False)
    return JsonResponse({'message': 'No input or invalid'}, safe=False)

