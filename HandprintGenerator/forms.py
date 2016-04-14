from django import forms
from .models import *
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth


class NewActionIdeaForm(forms.ModelForm):
    class Meta:
        model = ActionIdea
        fields = ['category','name', 'description', 'tags', 'references', 'image']
        exclude = ['creator', 'date_created', 'active']
        widgets = {
            'description': Textarea(attrs={'cols': 20, 'rows': 5}),
            'references': Textarea(attrs={'cols': 20, 'rows': 5}),
        }
        labels = { #Use labels to mark required fields.
            'name': ('Idea Title*'),
            'description': ('Describe your idea*'),
            'references': ('Any references or sources?'),
            'image': ('Upload an image related to your idea'),
            'category': ('Category*'),
            'tags': ('Submit some tags related to your idea'),

        } #Use text instead of tooltips or help icon to make it easier for mobile users.
        help_texts = {
            'name': ('A title should describe the main objective of an idea'),
            'description': ('What is your idea and how can people adopt it?'),
            'references': ('Any websites or additional information you want to include? Optional.'),
            'image': ('Optional, but adds some visual appeal.'),
            'category': ('What context does your idea apply to? Select one you think best fits.'),
            'tags': ('Any tags you enter will make your idea searchable by that tag. Use spaces or commas to separate tags.'),
        }

class DeleteActionIdeaForm(forms.ModelForm):
    class Meta:
        model = ActionIdeaInactive
        fields = ['reason']
        exclude = ['action_idea, date_create, responsible']

class SearchForm(forms.Form):
    searchTerm = forms.CharField(label='Search', max_length=100)

class CommentForm(forms.ModelForm):
    class Meta:
        model = ActionIdeaComment
        fields = ['text']
        exclude = ['date_created', 'action_idea', 'user']
        widgets = {
            'text': Textarea(attrs={'cols': 20, 'rows': 5}),
        }
        labels = {
            'text': ('Post a Comment'),
        }
        
class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

#from: http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username', 'password1', 'password2')
        exclude = ['first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(),
        }
        labels = { #Use labels to mark required fields.
            'username': ('Username'),
            'email': ('Email'),

        }
        help_texts = { #Use text instead of tooltips or help icon to make it easier for mobile users.
            'username': ('To login and will be displayed when you submit new ideas and comments.'),
            'email': ( 'To validate your account and reset your password.'),
        }


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        #user.first_name = self.cleaned_data["first_name"] Not asking for name.
        #user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user