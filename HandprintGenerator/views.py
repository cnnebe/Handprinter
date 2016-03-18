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

def user_index(request):
	context = {}
	context['users'] = User.objects.order_by('-date_created')#[:5]
    
	return render(request, 'HandprintGenerator/user_index.html', context)

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
    form = NewActionItemForm(request.POST)
    context['NewActionItemForm'] = form
    if form.is_valid():
        new_action_idea = form.save(commit=False)
        new_action_idea.date_created = datetime.datetime
        new_action_idea.save()
        return HttpResponseRedirect('.')

    return render(request, 'HandprintGenerator/new_action_idea.html', context)

@transaction.atomic
def new_user(request):
    context = {
        'users': User.objects.all(),
    }
    form = RegistrationForm(request.POST)
    context['registration_form'] = form
    #Validates the form.
    if form.is_valid():
        user = form.save(commit=False)
        user.date_created = datetime.datetime
        #user.location = 
        user.save()
        return HttpResponseRedirect('.')
        
    return render(request, 'HandprintGenerator/new_user.html', context)