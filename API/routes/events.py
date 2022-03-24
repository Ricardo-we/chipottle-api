from API.models import Events, Admins
from django.http import JsonResponse
from API.serializers import EventsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from API.utils import get_totals

def get_events(request):
    if(request.GET.get('id')):
        id = request.GET.get('id')
        all_events = Events.objects.filter(id=id)
        events = list(all_events.values())
        for i in range(len(all_events)):
            events[i]['event_image'] = all_events[i].event_image.url
    else: 
        all_events = Events.objects.all()
        events = list(all_events.values())
        for i in range(len(all_events)):
            events[i]['event_image'] = all_events[i].event_image.url

    return JsonResponse(events, safe=False)

def add_event(request):
    event_name = request.data.get('event-name')
    event_image = request.FILES.get('event-image')
    event = Events(event_name=event_name, event_image=event_image)
    event.save()
    return JsonResponse({'message': 'Event added'}, safe=False)

def delete_event(pk):
    Events.objects.filter(id=pk).delete()
    return JsonResponse({'message': 'Event deleted'})

def update_event(request, pk):
    event = Events.objects.get(id=pk)
    event.event_name = request.data.get('event-name')
    if(request.FILES.get('event-image')): event.event_image = request.FILES.get('event-image')
    event.save()
    return JsonResponse({'message': 'Sale deleted'}, safe=False)


@csrf_exempt
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def manage_events(request, pk=''):
    key = request.data.get('key')
    try:
        if(request.method == 'GET'):
            return get_events(request)
        elif(Admins.objects.get(admin_key=key)):
            if(request.method == 'POST'):
                return add_event(request)
            elif(request.method == 'PUT'):
                return update_event(request, pk)
            elif(request.method == 'DELETE'):
                return delete_event(pk)
    except:
        return JsonResponse({'message': 'Something went wrong, or invalid input'}, safe=False)
    return JsonResponse({'message': 'No input or invalid'}, safe=False)

