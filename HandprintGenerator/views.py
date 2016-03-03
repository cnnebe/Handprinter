from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the Handprint Generator index.")

def detail(request, action_item_id):
    return HttpResponse("You're looking at action item %s." % action_item_id)
