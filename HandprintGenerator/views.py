from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

from .models import * 
from .forms import *

import datetime

def index(request):
	context = {}
	context['action_ideas'] = ActionIdea.objects.order_by('-date_created')#[:5]

	#context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
	#context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
	#context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
	return render(request, 'HandprintGenerator/index.html', context)

#def index_by_cat(request):
#	context = {}
#	context['action_ideas'] = ActionIdea.objects.filter(category="home")

def user_index(request):
	context = {}
	context['users'] = User.objects.order_by('-date_joined')#[:5]
    
	return render(request, 'HandprintGenerator/user_index.html', context)

@transaction.atomic
def detail(request, actionidea_id):
    context = {}
    context['ai'] = get_object_or_404(ActionIdea, pk=actionidea_id)
    form = CommentForm(request.POST)
    context['comment_form'] = form
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.action_idea = ActionIdea.objects.get(pk=actionidea_id)
        new_comment.user_id = request.user.id
        new_comment.save()
        return HttpResponseRedirect('.')

    return render(request, 'HandprintGenerator/detail.html', context)


@transaction.atomic
def new_action_idea(request):
    context = {}
    if request.method == "POST":
        form = NewActionIdeaForm(request.POST)
        context['NewActionIdeaForm'] = form
        if form.is_valid():
            new_action_idea = form.save(commit=False)
            new_action_idea.date_created = datetime.datetime
            new_action_idea.creator_id = request.user.id
            new_action_idea.save()
            return HttpResponseRedirect('.')
    else:
        form = NewActionIdeaForm()
        context['NewActionIdeaForm'] = form

    return render(request, 'HandprintGenerator/new_action_idea.html', context)

@transaction.atomic
def new_user(request):
    context = {
        'users': User.objects.all(),
    }
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        context['registration_form'] = form
        #Validates the form.
        if form.is_valid():
            #create the objects and ties them together
            new_user = form.save(commit=False)
            new_user.save() 
            
            #creating an accompanying profile with role
            user_profile = Profile(role='Member', user_id=new_user.id)
            user_profile.save()
            
            return HttpResponseRedirect('/index')
    else:
        form = UserCreateForm()
        context['registration_form'] = form
        
    return render(request, 'registration/new_user.html', context)
    
def login(request):
    context = {}
    form = PickyAuthenticationForm(request.POST)
    context['form'] = form
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/index')

    return render(request, 'registration/login.html', context)

    
def logout(request):
    context = {}
    auth.logout(request)
    return render(request, 'registration/logout.html', context)