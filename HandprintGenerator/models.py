from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('admin', 'Administrator'), 
    ('mod', 'Moderator'), 
    ('member', 'Member'),
    )

CATEGORY_CHOICES = (
    ('home', 'Home'), 
    ('work', 'Work'), 
    ('community', 'Community'),
    ('food', 'Food'),
    ('mobility', 'Mobility'),
    ('clothing', 'Clothing'),
    ('other', 'Other')
    )

REASON_CHOICES = (
    ('duplicate', 'Duplicate'),
    ('accident', 'Accident'),
    ('spam', 'Spam'),
    ('inappropriate', 'Inappropriate'),
    ('inaccurate', 'Inaccurate'),
    ('other', 'Other')
    )

class Profile(models.Model):
    #we are using from Django's User class, and it has the following fields:
    #username
    #first_name
    #last_name
    #email
    #password
    #is_staff
    #is_active
    #is_superuser
    #last_login
    #date_joined
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = ROLE_CHOICES,
        default = 'member')

class ActionIdea(models.Model):
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    references = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.CharField(
        max_length = 15, 
        choices = CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    def numvotes(self):
        return ActionIdeaVote.objects.filter(action_idea=self.id).count()

    def comments(self):
        return ActionIdeaComment.objects.filter(action_idea=self.id).all()


class ActionIdeaComment(models.Model):
    action_idea = models.ForeignKey(ActionIdea)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

class ActionIdeaTag(models.Model):
    action_idea = models.ForeignKey(ActionIdea)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)

class ActionIdeaVote(models.Model):
    action_idea = models.ForeignKey(ActionIdea)
    user = models.ForeignKey(User)

class ActionIdeaInactive(models.Model):
    action_idea = models.ForeignKey(ActionIdea)
    reason = models.CharField(
        max_length = 15, 
        choices = REASON_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    responsible = models.ForeignKey(User)