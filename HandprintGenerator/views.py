from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db import transaction

from .models import * #ActionItem
from .forms import *

def index(request):
    alpha_action_item_list = ActionItem.objects.order_by('-name')[:5]
    context = {
        'alpha_action_item_list': alpha_action_item_list,
    }
    return render(request, 'HandprintGenerator/index.html', context)


def detail(request, actionitem_id):
    ai = get_object_or_404(ActionItem, pk=actionitem_id)
    return render(request, 'HandprintGenerator/detail.html', {'ai': ai})


# @transaction.atomic
# def new_action_item(request):
#     form = ActionItemForm()
# 	if request.method == 'POST':
#         form = NewActionItemForm(request.POST)
#         if form.is_valid():
#         	action_item = ActionItem.objects.create_action_item()
#         return render(request, 'HandprintGenerator/new.html', context)

# @transaction.atomic
# def create_user(request):
# 	#messages = []
# 	context = {
# 		'users': User.objects.all(),
# 	}

#     # Creates a bound form from the request POST parameters and makes the 
#     # form available in the request context dictionary.
# 	form = RegistrationForm(request.POST)
# 	context['registration_form'] = form

#     # Validates the form.
# 	#if not form.is_valid():
# 	#	return render(request, 'index.html', context)

# 	if form.is_valid():
# 		new_user = User.objects.create_user(username=form.cleaned_data['username'],
# 						first_name=form.cleaned_data['first_name'],
# 	                    last_name=form.cleaned_data['last_name'],
# 	                    password=form.cleaned_data['password'],
# 	                    email=form.cleaned_data['email']
# 	                    )

# 		new_user.save()

# 	#messages.append('Added {}'.format(new_user))
# 	return render(request, 'user.html', context)

#@transaction.atomic
# def new_action_item(request):
# 	if request.method == 'POST':
#         new_ai_form = new_action_idea.html
#         return render(request, 'HandprintGenerator/new.html', {'form1':rew_ai_form})

