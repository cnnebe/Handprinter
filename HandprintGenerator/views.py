from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


from .models import * 
from .forms import *
from django.db.models import Count

import datetime

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

def index_work(request):
    context = {}
    context['action_ideas_work_inactive'] = ActionIdea.objects.filter(active=False, category = 'work').order_by('-date_created')
    context['action_ideas_work_active'] = ActionIdea.objects.filter(active=True, category = 'work').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_work')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_work')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_work.html', context)

def index_food(request):
    context = {}
    context['action_ideas_food_inactive'] = ActionIdea.objects.filter(active=False, category = 'food').order_by('-date_created')
    context['action_ideas_food_active'] = ActionIdea.objects.filter(active=True, category = 'food').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_food')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_food')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_food.html', context)

def index_home(request):
    context = {}
    context['action_ideas_home_inactive'] = ActionIdea.objects.filter(active=False, category = 'home').order_by('-date_created')
    context['action_ideas_home_active'] = ActionIdea.objects.filter(active=True, category = 'home').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_home')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_home')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_home.html', context)

def index_community(request):
    context = {}
    context['action_ideas_community_inactive'] = ActionIdea.objects.filter(active=False, category = 'community').order_by('-date_created')
    context['action_ideas_community_active'] = ActionIdea.objects.filter(active=True, category = 'community').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_community')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_community')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_community.html', context)

def index_mobility(request):
    context = {}
    context['action_ideas_mobility_inactive'] = ActionIdea.objects.filter(active=False, category = 'mobility').order_by('-date_created')
    context['action_ideas_mobility_active'] = ActionIdea.objects.filter(active=True, category = 'mobility').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_mobility')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_mobility')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_mobility.html', context)

def index_clothing(request):
    context = {}
    context['action_ideas_clothing_inactive'] = ActionIdea.objects.filter(active=False, category = 'clothing').order_by('-date_created')
    context['action_ideas_clothing_active'] = ActionIdea.objects.filter(active=True, category = 'clothing').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_clothing')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_clothing')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_clothing.html', context)

def index_other(request):
    context = {}
    context['action_ideas_other_inactive'] = ActionIdea.objects.filter(active=False, category = 'other').order_by('-date_created')
    context['action_ideas_other_active'] = ActionIdea.objects.filter(active=True, category = 'other').order_by('-date_created') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_other')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_other')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_other.html', context)

def index_vote(request):
    context = {}
    context['action_ideas_vote_inactive'] = ActionIdea.objects.filter(active=False).annotate(num_votes=Count('actionideavote')).order_by('-num_votes')
    context['action_ideas_vote_active'] = ActionIdea.objects.filter(active=True).annotate(num_votes=Count('actionideavote')).order_by('-num_votes') #[:5]
    try:
        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
        return HttpResponseRedirect('/index_vote')
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
        v.save()
        return HttpResponseRedirect('/index_vote')

    #context['action_ideas_inactive'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #context['action_ideas']  = sorted(ActionIdea.objects.all(), key=lambda ai: ai.numvotes)
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    #context['action_ideas'] = ActionIdea.objects.order_by('-date_created')
    return render(request, 'HandprintGenerator/index_vote.html', context)

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
            return HttpResponseRedirect('/index')

    return render(request, 'registration/login.html', context)

    
def logout(request):
    context = {}
    auth.logout(request)
    return render(request, 'registration/logout.html', context)