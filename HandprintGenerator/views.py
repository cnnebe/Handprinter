from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction

from .models import * #ActionItem
from .forms import *

import datetime

def index(request):
    alpha_action_item_list = ActionItem.objects.order_by('-name')[:5]
    context = {
        'alpha_action_item_list': alpha_action_item_list,
    }
    return render(request, 'HandprintGenerator/index.html', context)


def detail(request, actionitem_id):
    ai = get_object_or_404(ActionItem, pk=actionitem_id)
    return render(request, 'HandprintGenerator/detail.html', {'ai': ai})


@transaction.atomic
def new_action_item(request):
    context = {}
    if request.method == 'POST':
        form = NewActionItemForm(request.POST)
        context['NewActionItemForm'] = form
        if form.is_valid():
            new_action_idea = form.save(commit=False)
            new_action_idea.date_created = datetime.datetime
            new_action_idea.active = True
            new_action_idea.save()
            #this is sending a user home after an action item is successfully created - we should probably send them to their new action idea instead?
            return HttpResponseRedirect('HandprintGenerator/')
        
    else: #this is triggered when there isn't a POST request - aka arriving at the page for the first time, which is a GET request. In this case, we want to 
        form = NewActionItemForm()
        
    return render(request, 'HandprintGenerator/new_action_idea.html', {'form': form}, context)

#@transaction.atomic
#def create_user(request):
#    context = {
#        'users': User.objects.all(),
#    }

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
#    form = RegistrationForm(request.POST)
#    context['registration_form'] = form

    #Validates the form.
#    if not form.is_valid():
#        return render(request, 'index.html', context)

 #   if form.is_valid():
 #       new_user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])

#    new_user.save()

#    return render(request, 'user.html', context)