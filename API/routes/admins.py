from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from API.models import Admins
from API.utils import generate_admin_key

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def admin_login(request):
    key = request.POST.get('key')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if(key):
        if(Admins.objects.get(admin_key=key)):
            return add_admin(request)
    
    admin = Admins.objects.filter(username=username, password=password, email=email)
    if(admin.exists()):
        return JsonResponse(admin.values().first(), safe=False)
    return JsonResponse({'message': 'Invalid user data'}, safe=False)

def get_admins():
    admins = list(Admins.objects.all().values())
    return JsonResponse(admins, safe=False)

def add_admin(request):
    admin = Admins(
        username=request.data.get('username'), 
        password=request.data.get('password'), 
        email=request.data.get('email'), 
        admin_key=generate_admin_key(Admins.objects.all())
    )

    if(admin.username and admin.password and admin.email): 
        admin.save()
        return JsonResponse({'message': 'New admin added successfully'}, safe=False)
        
    return JsonResponse({'message': 'invalid'}, safe=False)

def remove_admin(pk):
    deleted_admin = Admins.objects.get(id=pk)
    deleted_admin.delete()
    return JsonResponse({'message': 'Admin deleted successfully'}, safe=False)


def update_admin(request, pk):
    try:
        admin = Admins.objects.get(id=pk)
        admin.username = request.data.get('username') 
        admin.password = request.data.get('password')
        admin.email = request.data.get('email')
        admin.save()
        return JsonResponse({'message': 'Admin updated successfully'}, safe=False)
    except:
        return JsonResponse({'message': 'Invalid changes'}, safe=False)

@api_view(['POST','DELETE', 'PUT'])
@parser_classes([MultiPartParser])
@csrf_exempt
def manage_admins(request, pk=''):
    key = request.data.get('key')
    
    if(Admins.objects.get(admin_key=key)):
        if(request.method == 'POST' and request.GET.get('get-admins')):
            return get_admins()
        elif(request.method == 'POST'):
            return add_admin(request)
        elif(request.method == 'DELETE'):
            return remove_admin(pk)
        elif(request.method == 'PUT'):
            return update_admin(request, pk)
        
