from django import forms
from .models import *
from django.forms import ModelForm


class NewActionItemForm(forms.ModelForm):
    class Meta:
        model = ActionItem
        fields = ['creator', 'name', 'description', 'references', 'images', 'category']
        exclude = ['date_created', 'active']
        widgets = {
            'description': forms.Textarea(),
            'references': forms.Textarea(),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = ActionItemComment
        fields = ['text', 'user']
        exclude = ['date_created', 'action_item']
        widgets = {
            'text': forms.Textarea(),
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        exclude = ['date_created', 'location', 'role', 'last_login']
        widgets = {
            'password': forms.PasswordInput(),
        }

#    def clean(self):
#        cleaned_data = super(RegistrationForm, self).clean()

#        username = cleaned_data['username']
#        password = cleaned_data['password']
#        if len(password) < 8:
#            raise forms.ValidationError('Password must be more than 8 characters in length')
#        return cleaned_data

    # def clean_username(self):
    #     username = self.cleaned_data['username']

    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Student already exists.')

    #     return username

    # def clean_password(self):
    #     password = self.cleaned_data['password']

    #     if len(password) < 8:
    #         raise forms.ValidationError('Password must be more than 8 characters in length')

    #     return password