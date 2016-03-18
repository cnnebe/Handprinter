from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction

from .models import * 
from .forms import *

import datetime

def index(request):
	context = {}
	context['action_items'] = ActionItem.objects.order_by('-date_created')#[:5]

	#context['action_items']  = sorted(ActionItem.objects.all(), key=lambda ai: ai.numvotes)
	#context['action_items'] = ActionItem.objects.order_by('-date_created')
	#context['action_items'] = ActionItem.objects.order_by('-date_created')
	return render(request, 'HandprintGenerator/index.html', context)

#def index_by_cat(request):
#	context = {}
#	context['action_items'] = ActionItem.objects.filter(category="home")

@transaction.atomic
def detail(request, actionitem_id):
	context = {}
	context['ai'] = get_object_or_404(ActionItem, pk=actionitem_id)
	form = CommentForm(request.POST)
	context['comment_form'] = form
	if form.is_valid():
		new_comment = form.save(commit=False)
		new_comment.action_item = ActionItem.objects.get(pk=actionitem_id)
		new_comment.save()
		return HttpResponseRedirect('.')

	return render(request, 'HandprintGenerator/detail.html', context)


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