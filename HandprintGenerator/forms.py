from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth


class NewActionItemForm(forms.ModelForm):
    class Meta:
        model = ActionItem
        fields = ['name', 'description', 'references', 'images', 'category']
        exclude = ['creator', 'date_created', 'active']
        widgets = {
            'description': forms.Textarea(),
            'references': forms.Textarea(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = ActionItemComment
        fields = ['text']
        exclude = ['date_created', 'action_item', 'user']
        widgets = {
            'text': forms.Textarea(),
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
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user