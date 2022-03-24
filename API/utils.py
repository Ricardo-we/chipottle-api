import random
from .models import Products, Sales

def generate_admin_key(admins):
    numbers_and_letters = 'abcdefghijklmnopqrstxyz0123456789'
    new_key = ''
    while len(new_key) <= 20:
        for i in range(255 // 5):
            new_key += random.choice(numbers_and_letters)
            new_key += random.choice(numbers_and_letters)
        for admin in admins:
            if admin.admin_key == new_key:
                new_key = ''    
    return new_key

def get_total_sales():
    sales = Sales.objects.all()
    total_sales = 0
    for sale in sales:
        total_sales += sale.sold_product.item_price
    return total_sales
    
def get_totals(product_name):
    product = Products.objects.get(item_name=product_name)
    sales = Sales.objects.filter(sold_product=product).all()
    total_sales = 0
    for sale in sales:
        total_sales += sale.sold_product.item_price
    return total_sales
