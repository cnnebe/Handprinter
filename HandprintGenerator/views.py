from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import ActionItem

def index(request):
    alpha_action_item_list = ActionItem.objects.order_by('-name')[:5]
    context = {
        'alpha_action_item_list': alpha_action_item_list,
    }
    return render(request, 'HandprintGenerator/index.html', context)


def detail(request, actionitem_id):
    ai = get_object_or_404(ActionItem, pk=actionitem_id)
    return render(request, 'HandprintGenerator/detail.html', {'ai': ai})