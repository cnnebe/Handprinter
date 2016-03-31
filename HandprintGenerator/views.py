from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .models import * 
from .forms import *

import datetime
import string
import random

def home(request):
    context = {}
    return render(request, 'HandprintGenerator/home.html', context)

def index(request):
    context = {}
    context['action_ideas_inactive'] = ActionIdea.objects.filter(active=False).order_by('-date_created')
    context['action_ideas_active'] = ActionIdea.objects.filter(active=True).order_by('-date_created')#[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
	#context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
	#context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
	#context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index.html', context)

@transaction.atomic
def detail(request, actionidea_id):
    context = {}
    context['ai'] = get_object_or_404(ActionIdea, pk=actionidea_id)
    try:
        context['userVote'] = ActionIdeaVote.objects.get(user=request.user, action_idea = ActionIdea.objects.get(pk=actionidea_id))
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user).delete()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user)
        v.save()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    form = CommentForm(request.POST)
    context['comment_form'] = form
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.action_idea = ActionIdea.objects.get(pk=actionidea_id)
            new_comment.user_id = request.user.id
            new_comment.save()
            return HttpResponseRedirect('.')

    return render(request, 'HandprintGenerator/detail.html', context)

@login_required
@transaction.atomic
#using this as edit and create action idea form
def edit_action_idea(request, actionidea_id=None):
    context = {}
    if actionidea_id: #ediing action idea
        action_idea = get_object_or_404(ActionIdea, pk = actionidea_id)
    else: #new action idea
        action_idea = ActionIdea(date_created = datetime.datetime, creator_id = request.user.id)
    
    form = NewActionIdeaForm(request.POST or None, instance=action_idea)
    if request.method == "POST":
        context['NewActionIdeaForm'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/index')
    else:
        context['NewActionIdeaForm'] = form

    return render(request, 'HandprintGenerator/new_action_idea.html', context)

@login_required
@transaction.atomic
def delete_action_idea(request, actionidea_id):
    context = {}
    form = DeleteActionIdeaForm(request.POST)
    context['DeleteActionIdeaForm'] = form
    if form.is_valid():
        delete_ai = form.save(commit=False)
        delete_ai.date_created = datetime.datetime
        delete_ai.responsible = request.user
        delete_ai.action_idea = ActionIdea.objects.get(pk=actionidea_id)
        delete_ai.save()

        action_idea = get_object_or_404(ActionIdea, pk = actionidea_id)
        action_idea.active = False
        action_idea.save()
        return HttpResponseRedirect('/index')
    else:
        form = DeleteActionIdeaForm()
        context['DeleteActionIdeaForm'] = form

    return render(request, 'HandprintGenerator/delete_action_idea.html', context)   

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
            
            return HttpResponseRedirect('/login')
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
            return HttpResponseRedirect('/index/')

    return render(request, 'registration/login.html', context)

    
def logout(request):
    context = {}
    auth.logout(request)
    return render(request, 'registration/logout.html', context)
    
def forgot_password(request):
    context = {}
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
            #see if the person's email matches an actual user
            forgotten_user = User.objects.get(email=user_email)
            #now generate a random string to reset their password to
            #from: http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
            new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            #now reset their password
            forgotten_user.set_password(new_password)
            forgotten_user.save()
            #now put the password in an email message
            password_message = """Hi %s,
            
You recently requested to reset your password for your Handprint Generator account. We have reset your password. Your new, temporary password is:

%s

If you did not request a password reset, please reply to let us know. We urge you to change your password upon logging in by going to user profile and editing your password.

Thanks,
The Handprinter Team

P.S. We also love hearing from you and assisting you with any concerns you may have. Please reply to this email if you want to ask a question or submit a comment.
""" % (forgotten_user.first_name, new_password)
            #now send them an email with the new password
            send_mail('Handprinter Password Reset', password_message, 'bcg06770@yahoo.com',
    [user_email], fail_silently=False)
            
            return render(request, 'registration/forgot_password_success.html', context)
        except:
            #it didn't work, let the user know
            return render(request, 'registration/forgot_password_failure.html', context)

    return render(request, 'registration/forgot_password.html', context)