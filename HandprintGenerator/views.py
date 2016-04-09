from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.gis import geoip2
from django.contrib.gis.geoip2 import GeoIP2

from .models import * 
from .forms import *

import datetime
import string
import random

def home(request):
    context = {}
    return render(request, 'HandprintGenerator/home.html', context)

def user_profile(request):
    try:
        context = {}
        context['myideas'] = ActionIdea.objects.filter(creator=request.user, active=True).order_by('-date_created')
        context['mycomments'] = ActionIdeaComment.objects.filter(user = request.user)
        context['myvotes'] = ActionIdeaVote.objects.filter(user = request.user)
        if request.method == "POST":
            if request.POST.get('change_email') and request.POST.get('change_email') != '':
                u = User.objects.get(id=request.user.id)
                u.email = request.POST.get('change_email')
                u.save()
                return HttpResponseRedirect('/logout')
        if request.method == "POST":
            if request.POST.get('change_password') and request.POST.get('change_password') != '':
                if request.POST.get('change_password') != request.POST.get('change_password_confirmation'):
                    return HttpResponseRedirect('/profile')
                u = User.objects.get(id=request.user.id)
                u.set_password(request.POST.get('change_password'))
                u.save()
                return HttpResponseRedirect('/logout')
    except:
        pass
    return render(request, 'HandprintGenerator/user_profile.html', context)

def index(request):
    # Action Idea Objects divided by activity and sorted by category, popularity and most recent. 
    context = {}
    context['action_ideas_inactive'] = ActionIdea.objects.filter(active=False).order_by('-date_created')
    context['action_ideas_active'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    context['action_ideas_work_inactive'] = ActionIdea.objects.filter(active=False, category = 'work').order_by('-date_created')
    context['action_ideas_work_active'] = ActionIdea.objects.filter(active=True, category = 'work').order_by('-date_created')
    context['action_ideas_food_inactive'] = ActionIdea.objects.filter(active=False, category = 'food').order_by('-date_created')
    context['action_ideas_food_active'] = ActionIdea.objects.filter(active=True, category = 'food').order_by('-date_created')
    context['action_ideas_community_inactive'] = ActionIdea.objects.filter(active=False, category = 'community').order_by('-date_created')
    context['action_ideas_community_active'] = ActionIdea.objects.filter(active=True, category = 'community').order_by('-date_created') 
    context['action_ideas_home_inactive'] = ActionIdea.objects.filter(active=False, category = 'home').order_by('-date_created')
    context['action_ideas_home_active'] = ActionIdea.objects.filter(active=True, category = 'home').order_by('-date_created') 
    context['action_ideas_clothing_inactive'] = ActionIdea.objects.filter(active=False, category = 'clothing').order_by('-date_created')
    context['action_ideas_clothing_active'] = ActionIdea.objects.filter(active=True, category = 'clothing').order_by('-date_created') 
    context['action_ideas_mobility_inactive'] = ActionIdea.objects.filter(active=False, category = 'mobility').order_by('-date_created')
    context['action_ideas_mobility_active'] = ActionIdea.objects.filter(active=True, category = 'mobility').order_by('-date_created') 
    context['action_ideas_other_inactive'] = ActionIdea.objects.filter(active=False, category = 'other').order_by('-date_created')
    context['action_ideas_other_active'] = ActionIdea.objects.filter(active=True, category = 'other').order_by('-date_created') 
    context['action_ideas_vote_inactive'] = ActionIdea.objects.filter(active=False).annotate(num_votes=Count('actionideavote')).order_by('-num_votes')
    context['action_ideas_vote_active'] = ActionIdea.objects.filter(active=True).annotate(num_votes=Count('actionideavote')).order_by('-num_votes') 
    
    #Voting Functionality
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

    #Search Functionality
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['SearchTerm']
            print(search_term)
            print(ActionIdea.objects.filter(tags__name__in=[search_term]))    
            context['action_ideas_search_active'] = ActionIdea.objects.filter(tags__name = search_term)
            return HttpResponseRedirect('/HandprintGenerator/searchresults/')

    return render(request, 'HandprintGenerator/index.html', context)

@transaction.atomic
def detail(request, actionidea_id):
    context = {}
    context['ai'] = get_object_or_404(ActionIdea, pk=actionidea_id)
    try:
        context['userVote'] = ActionIdeaVote.objects.get(user=request.user, action_idea = ActionIdea.objects.get(pk=actionidea_id))
    except:
        context['userVote'] = False
    try: 
        context['reason'] = ActionIdeaInactive.objects.get(action_idea = ActionIdea.objects.get(pk=actionidea_id))
    except: 
        context['reason'] = False
    if request.POST.get('restore'):
        ai = ActionIdea.objects.get(pk=actionidea_id)
        ai.active = True
        ai.save()
        ActionIdeaInactive.objects.get(action_idea = ai).delete()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('unvote'):
        ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user).delete()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('vote'):
        v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user)
        v.save()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('delete'):
        c = get_object_or_404(ActionIdeaComment, pk = request.POST.get('comment')).delete()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('report'):
        action_idea = context['ai']
        report_message = """Hi Handprinter Admin Team,
            
There has been an action idea reported as inappropriate.

Action Idea ID: %d
Action Idea Title: %s
Action Idea Description: %s
Action Idea References: %s

For your reference, the user who reported this is: %s

Thanks,
The Handprinter Team
""" % (action_idea.id, action_idea.name, action_idea.description, action_idea.references, request.user.username)
        send_mail('Reported Action Idea', report_message, 'actions@handprinter.org', ['actions@handprinter.org',], fail_silently=False)
        return HttpResponseRedirect('/index')
    if request.POST.get('report_comment'):
        action_idea = context['ai']
        c = request.POST.get('comment_reported')
        comment = ActionIdeaComment.objects.get(id = c)
        report_message = """Hi Handprinter Admin Team,
            
There has been a comment reported as inappropriate.

Comment ID: %d
Comment Text: %s
Comment Creator: %s
Action Idea ID: %d
Action Idea Name: %s

For your reference, the user who reported this is: %s

Thanks,
The Handprinter Team
""" % (comment.id, comment.text, User.objects.get(id = comment.user_id).username, action_idea.id, action_idea.name, request.user.username)
        send_mail('Reported Action Idea Comment', report_message, 'actions@handprinter.org', ['actions@handprinter.org',], fail_silently=False)
        return HttpResponseRedirect('/index')
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


def search_results(request):
    context = {}
    form = SearchForm(request.GET)
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
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['searchTerm']
            context['search_term'] = search_term
            context['ai_search_active'] = ActionIdea.objects.filter(active=True, tags__name__in=[search_term]).order_by('-date_created')
            context['ai_search_inactive'] = ActionIdea.objects.filter(active=False, tags__name__in=[search_term]).order_by('-date_created')
            return render(request, 'HandprintGenerator/searchresults.html', context)
    return render(request, 'HandprintGenerator/searchresults.html', context)

@login_required
@transaction.atomic
def edit_action_idea(request, actionidea_id=None):
    context = {}
    if actionidea_id: #editing action idea
        action_idea = get_object_or_404(ActionIdea, pk = actionidea_id)
    else: #new action idea
        action_idea = ActionIdea(date_created = datetime.datetime, creator_id = request.user.id)
    
    form = NewActionIdeaForm(request.POST or None, request.FILES or None, instance=action_idea)
    context['creator'] = action_idea.creator_id
    context['active'] = action_idea.active
    if request.method == "POST":
        context['NewActionIdeaForm'] = form
        if form.is_valid():
            #form.image = request.FILES['image']
            form.save()
            return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    else:
        context['NewActionIdeaForm'] = form
        context['action_id'] = actionidea_id

    return render(request, 'HandprintGenerator/new_action_idea.html', context)

@login_required    
@transaction.atomic
def new_action_idea(request):
    context = {}
    if request.method == "POST":
        action_idea = ActionIdea(date_created = datetime.datetime, creator_id = request.user.id)
        form = NewActionIdeaForm(request.POST, request.FILES, instance=action_idea)
        context['NewActionIdeaForm'] = form
        if form.is_valid():
            new_action_idea = form.save(commit=False)
            new_action_idea.save()
            form.save_m2m()
            return HttpResponseRedirect('/index')
    else:
        form = NewActionIdeaForm()
        context['NewActionIdeaForm'] = form

    return render(request, 'HandprintGenerator/new_action_idea.html', context)

@login_required
@transaction.atomic
def delete_action_idea(request, actionidea_id):
    context = {}
    form = DeleteActionIdeaForm(request.POST)
    context['DeleteActionIdeaForm'] = form
    context['ActionIdea'] = ActionIdea.objects.get(pk=actionidea_id)
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
            if User.objects.filter(email = new_user.email ).exists():
                context["error"] = "error"
                return render(request, 'registration/new_user.html', context)
            new_user.save() 
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            if ip == '127.0.0.1':
                ip = '72.14.207.99'
            g = GeoIP2()
            g = g.city(ip)
            loc = g['city'] + ', ' + g['region'] + ', ' + g['country_name']
            
            #creating an accompanying profile with role
            user_profile = Profile(role='member', location=loc, user_id=new_user.id)
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

For your reference, your username is: %s

Thanks,
The Handprinter Team

P.S. We also love hearing from you and assisting you with any concerns you may have. Please reply to this email if you want to ask a question or submit a comment.
""" % (forgotten_user.first_name, new_password, forgotten_user.username)
            #now send them an email with the new password
            send_mail('Handprinter Password Reset', password_message, 'actions@handprinter.org',
    [user_email], fail_silently=False)
            
            return render(request, 'registration/forgot_password_success.html', context)
        except:
            #it didn't work, let the user know
            return render(request, 'registration/forgot_password_failure.html', context)

    return render(request, 'registration/forgot_password.html', context)
