#for django things
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.gis import geoip2
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#for email 
import os
import email
import smtplib 
from email.mime.text import MIMEText
from django.conf import settings

#our other django files
from .models import * 
from .forms import *

#helpful python packages
import datetime
import string
import random

#for image uploading (Heroku cloudinary add-on)
import cloudinary
import cloudinary.uploader
import cloudinary.api

def home(request):
    context = {}
    return render(request, 'HandprintGenerator/home.html', context)

def user_profile(request):
    try:
        context = {}
        context['myideas'] = ActionIdea.objects.filter(creator=request.user, active=True).order_by('-date_created')
        context['myideasinactive'] = ActionIdea.objects.filter(creator=request.user, active=False).order_by('-date_created')
        for ideas in context:
            paginate(context, ideas, request)
        #Only show content of existing ideas
        context['mycomments'] = ActionIdeaComment.objects.filter(user = request.user, action_idea__active=True)
        context['myvotes'] = ActionIdeaVote.objects.filter(user = request.user, action_idea__active=True)
        if request.method == "POST":
            if request.POST.get('change_email') and request.POST.get('change_email') != '':
                u = User.objects.get(id=request.user.id)
                u.email = request.POST.get('change_email')
                u.save()
                messages.add_message(request, messages.SUCCESS, 'Email changed!')
                return HttpResponseRedirect('/logout')
        if request.method == "POST":
            if request.POST.get('change_password') and request.POST.get('change_password') != '':
                if request.POST.get('change_password') != request.POST.get('change_password_confirmation'):
                    messages.add_message(request, messages.ERROR, 'Passwords do not match')
                    return HttpResponseRedirect('/profile')
                u = User.objects.get(id=request.user.id)
                u.set_password(request.POST.get('change_password'))
                u.save()
                messages.add_message(request, messages.SUCCESS, 'Password changed!')
                return HttpResponseRedirect('/logout')
        if request.method == "POST":   
            if request.POST.get('change_location'): 
                p = User.objects.get(id=request.user.id).profile
                p.location = request.POST.get('change_location')
                p.save()
                messages.add_message(request, messages.SUCCESS, 'Location changed!')
                return HttpResponseRedirect('/profile')
    except:
        pass
    return render(request, 'HandprintGenerator/user_profile.html', context)

##################################### Action Idea Index and Search Views ###########################################

#The main action idea index (most recent)
def index(request):
    context = {}
    context['action_ideas_inactive'] = ActionIdea.objects.filter(active=False).order_by('-date_created')
    context['action_ideas_active'] = ActionIdea.objects.filter(active=True).order_by('-date_created')
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)   
    return render(request, 'HandprintGenerator/index.html', context)

#Generates search results page on search.
def search_results(request):
    context = {} 
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['searchTerm']
            context['search_term'] = search_term
            context['ai_search_active'] = ActionIdea.objects.filter(active=True, tags__name__in=[search_term]).order_by('-date_created')
            context['ai_search_inactive'] = ActionIdea.objects.filter(active=False, tags__name__in=[search_term]).order_by('-date_created')    
            context['header'] = "Search Results for \"%s\"" % search_term 
            context['paginate'] = False #Pagination does not work for search results due to GET request handling for each page.  
            return render(request, 'HandprintGenerator/searchresults.html', context)
    return HttpResponseRedirect('/index')

#Filter by category 'most popular'
def index_popular(request):
    context = {}
    context['action_ideas_vote_inactive'] = ActionIdea.objects.filter(active=False).annotate(num_votes=Count('actionideavote')).order_by('-num_votes')
    context['action_ideas_vote_active'] = ActionIdea.objects.filter(active=True).annotate(num_votes=Count('actionideavote')).order_by('-num_votes') 
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_popular.html', context)

#Filter by category 'home'
def index_home(request):
    context = {}
    context['action_ideas_home_inactive'] = ActionIdea.objects.filter(active=False, category = 'home').order_by('-date_created')
    context['action_ideas_home_active'] = ActionIdea.objects.filter(active=True, category = 'home').order_by('-date_created') 
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_home.html', context)

#Filter by category 'work'
def index_work(request):
    context = {}
    context['action_ideas_work_inactive'] = ActionIdea.objects.filter(active=False, category = 'work').order_by('-date_created')
    context['action_ideas_work_active'] = ActionIdea.objects.filter(active=True, category = 'work').order_by('-date_created')  
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_work.html', context)

#Filter by category 'community'
def index_community(request):
    context = {}
    context['action_ideas_community_inactive'] = ActionIdea.objects.filter(active=False, category = 'community').order_by('-date_created')
    context['action_ideas_community_active'] = ActionIdea.objects.filter(active=True, category = 'community').order_by('-date_created')    
    #Pagination
    for ideas in context:
        paginate(context, ideas, request) 
    return render(request, 'HandprintGenerator/index_community.html', context)

#Filter by category 'mobility'
def index_mobility(request):
    context = {}
    context['action_ideas_mobility_inactive'] = ActionIdea.objects.filter(active=False, category = 'mobility').order_by('-date_created')
    context['action_ideas_mobility_active'] = ActionIdea.objects.filter(active=True, category = 'mobility').order_by('-date_created')    
    #Pagination
    for ideas in context:
        paginate(context, ideas, request) 
    return render(request, 'HandprintGenerator/index_mobility.html', context)

#Filter by category 'food'
def index_food(request):
    context = {}
    context['action_ideas_food_inactive'] = ActionIdea.objects.filter(active=False, category = 'food').order_by('-date_created')
    context['action_ideas_food_active'] = ActionIdea.objects.filter(active=True, category = 'food').order_by('-date_created')  
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_food.html', context)

#Filter by category 'clothing'
def index_clothing(request):
    context = {}
    context['action_ideas_clothing_inactive'] = ActionIdea.objects.filter(active=False, category = 'clothing').order_by('-date_created')
    context['action_ideas_clothing_active'] = ActionIdea.objects.filter(active=True, category = 'clothing').order_by('-date_created') 
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_clothing.html', context)

#Filter by category 'other'
def index_other(request):
    context = {}
    context['action_ideas_other_inactive'] = ActionIdea.objects.filter(active=False, category = 'other').order_by('-date_created')
    context['action_ideas_other_active'] = ActionIdea.objects.filter(active=True, category = 'other').order_by('-date_created')   
    #Pagination
    for ideas in context:
        paginate(context, ideas, request)
    return render(request, 'HandprintGenerator/index_other.html', context)

def paginate(context, index, request):
    #Displays 5 ideas at a time per page.
    paginator = Paginator(context[index], 5)
    page = request.GET.get('page')
    try:
        context[index] = paginator.page(page)
    except PageNotAnInteger:
        context[index] = paginator.page(1)
    except EmptyPage:
        context[index] = paginator.page(paginator.num_pages)
    return 

###################################### View, Edit, and Delete Ideas ###############################################

@transaction.atomic
def detail(request, actionidea_id):
    context = {}
    context['ai'] = get_object_or_404(ActionIdea, pk=actionidea_id)

    #Voting
    try:
        context['userVote'] = ActionIdeaVote.objects.get(user=request.user, action_idea = ActionIdea.objects.get(pk=actionidea_id))
    except:
        context['userVote'] = False
    if request.POST.get('unvote'):
        is_current_vote = ActionIdeaVote.objects.filter(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user)
        if is_current_vote:
            messages.add_message(request, messages.SUCCESS, 'Idea Unvoted.')
            ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user).delete()
        else: 
            messages.add_message(request, messages.ERROR, 'You cannot unvote an idea you have not voted for!')
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    if request.POST.get('vote'):
        #If there is a current vote by this user, the user cannot vote again.
        is_current_vote = ActionIdeaVote.objects.filter(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user)
        if not is_current_vote:
            v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=actionidea_id), user = request.user)
            messages.add_message(request, messages.SUCCESS, 'Thank you for voting!')
            v.save()
        else:
            messages.add_message(request, messages.ERROR, 'You already voted for this idea!')
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)
    
    # Reason if idea is inactive.
    try: 
        context['reason'] = ActionIdeaInactive.objects.get(action_idea = ActionIdea.objects.get(pk=actionidea_id))
    except: 
        context['reason'] = False

    #Restore.
    if request.POST.get('restore'):
        ai = ActionIdea.objects.get(pk=actionidea_id)
        ai.active = True
        ai.save()
        ActionIdeaInactive.objects.get(action_idea = ai).delete()
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)

    #Report Idea.
    if request.POST.get('report'):
        action_idea = context['ai']
        msg = MIMEText("""Hi Handprinter Admin Team,
            
        There has been an action idea reported as inappropriate.

        Action Idea ID: %d
        Action Idea Title: %s
        Action Idea Description: %s
        Action Idea References: %s

        For your reference, the user who reported this is: %s

Thanks,
The Handprinter Team
""" % (action_idea.id, action_idea.name, action_idea.description, action_idea.references, request.user.username))
        msg['Subject'] = "Reported Action Idea"
        msg['From']    = "actions@handprinter.org"
        msg['To']      = "actions@handprinter.org"
        s = smtplib.SMTP(os.environ['MAILGUN_SMTP_SERVER'], os.environ['MAILGUN_SMTP_PORT'])
        s.login(os.environ['MAILGUN_SMTP_LOGIN'], os.environ['MAILGUN_SMTP_PASSWORD'])
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()
        messages.add_message(request, messages.SUCCESS, 'Idea Reported!')
        
        return HttpResponseRedirect('/index')

    #Report Comment.
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
        messages.add_message(request, messages.SUCCESS, 'Comment Reported!')
        return HttpResponseRedirect('/index')

    #Comment Display and Implementation
    form = CommentForm(request.POST)
    context['comment_form'] = form
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.action_idea = ActionIdea.objects.get(pk=actionidea_id)
            new_comment.user_id = request.user.id
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for commenting!')
            return HttpResponseRedirect('.')

    if request.POST.get('delete'):
        c = get_object_or_404(ActionIdeaComment, pk = request.POST.get('comment')).delete()
        messages.add_message(request, messages.SUCCESS, 'Comment Deleted!')
        return HttpResponseRedirect('/handprintgenerator/%s/' % actionidea_id)

    return render(request, 'HandprintGenerator/detail.html', context)

@login_required
@transaction.atomic
# Edit option is displayed in the details page of an action idea.
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
            form.save(commit=False)
            #image is uploaded locally, now upload to Heroku cloudinary
            new_image = cloudinary.uploader.upload(form.image, crop = 'limit', width = 2000)
            #set the new image URL on cloudinary
            form.image = new_image['url']
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Action Idea Edited!')
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
            #image is uploaded locally, now upload to Heroku cloudinary
            new_image = cloudinary.uploader.upload(new_action_idea.image, crop = 'limit', width = 2000)
            #set the new image URL on cloudinary
            new_action_idea.image = new_image['url']
            new_action_idea.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Action Idea Created! Click it to view details, comment, vote, or make changes.')
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
        messages.add_message(request, messages.SUCCESS, 'Action Idea Deleted!')
        return HttpResponseRedirect('/index')
    else:
        form = DeleteActionIdeaForm()
        context['DeleteActionIdeaForm'] = form
    return render(request, 'HandprintGenerator/delete_action_idea.html', context)   

########################################### Authentication Views ###############################################
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

            #Location Gathering using GeoIP2
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
            messages.add_message(request, messages.SUCCESS, 'Account created. Please login!')         
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
        #Inactive User attempting to login.
        elif user is not None and user is not user.is_active:
            messages.add_message(request, messages.ERROR, 'Your account has been deleted. Please contact staff for assistance.')
            HttpResponseRedirect('/login')
        #Incorrect Login Credentials.
        elif user is None:
            messages.add_message(request, messages.ERROR, 'The information you entered does not match any account.')
            HttpResponseRedirect('/login')
    return render(request, 'registration/login.html', context)

    
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'You have been logged out!')
    return render(request, 'registration/logout.html')
    
def forgot_password(request):
    context = {}
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
            # Match submitted email to a user's email who is active in the system.
            forgotten_user = User.objects.get(email=user_email, active=True)
            # Generates a random string to set as the new password upon reset.
            #from: http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
            new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            # Save generated password as the user's new password.
            forgotten_user.set_password(new_password)
            forgotten_user.save()
            # Email Message containing username and password.
            password_message = """Hi %s,
            
You recently requested to reset your password for your Handprint Generator account. We have reset your password. Your new, temporary password is:

%s

If you did not request a password reset, please reply to let us know. We urge you to change your password upon logging in by going to user profile and editing your password.

For your reference, your username is: %s

Thanks,
The Handprinter Team

P.S. We also love hearing from you and assisting you with any concerns you may have. Please reply to this email if you want to ask a question or submit a comment.
""" % (forgotten_user.username, new_password, forgotten_user.username)
            # Sends an email with the new password
            send_mail('Handprinter Password Reset', password_message, 'handprinterteam@yahoo.com',
                [user_email], fail_silently=False)
            messages.add_message(request, messages.SUCCESS,'An email has been sent to the address given. Please follow the instructions in the email.')
            # Redirect to login and displays success message.
            return render(request, 'registration/login.html', context)
        except:
            # Email not found in system. Allow user to try again and give error.
            messages.add_message(request, messages.ERROR,'The email given is not associated with an account or your account is banned. Please try again or create a new account.')
            return render(request, 'registration/forgot_password.html', context)

    return render(request, 'registration/forgot_password.html', context)


##Voting Logic for all index and search results pages
##To implement vote on index pages, call vote(request, context) on each index page and search page. 
#def vote(request, context):
#    #Populate Vote History
#    try:
#        context['userVotes'] = ActionIdeaVote.objects.filter(user=request.user).values_list('action_idea', flat=True)
#    except:
#        context['userVote'] = False
#    #Handle Vote/Unvote Requests
#    if request.POST.get('unvote'):
#        #If there is no existing vote by this user, then you cannot unvote. 
#        is_current_vote = ActionIdeaVote.objects.filter(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
#        if is_current_vote:
#            messages.add_message(request, messages.SUCCESS, 'Idea Unvoted.')
#            ActionIdeaVote.objects.get(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user).delete()
#        else: 
#            messages.add_message(request, messages.ERROR, 'You cannot unvote an idea you have not voted for!')
#    if request.POST.get('vote'):
#        #If there is a current vote by this user, the user cannot vote again.
#        is_current_vote = ActionIdeaVote.objects.filter(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
#        if not is_current_vote:
#            v = ActionIdeaVote(action_idea = ActionIdea.objects.get(pk=request.POST.get('action_idea')), user = request.user)
#            messages.add_message(request, messages.SUCCESS, 'Thank you for voting!')
#            v.save()
#        else:
#           messages.add_message(request, messages.ERROR, 'You already voted for this idea!')
#    return