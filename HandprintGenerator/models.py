from django.db import models

ROLE_CHOICES = (
    ('admin', 'Administrator'), 
    ('mod', 'Moderator'), 
    ('member', 'Member'),
    )

CATEGORY_CHOICES = (
    ('home', 'Home'), 
    ('work', 'Work'), 
    ('commute', 'Commute'),
    ('other', 'Other')
    )


class User(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    role = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = ROLE_CHOICES,
        default = 'member')

class ActionItem(models.Model):
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    references = models.CharField(max_length=500)
    images = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = CATEGORY_CHOICES)

class ActionItemComment(models.Model):
    action_item = models.ForeignKey(ActionItem)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

class ActionItemTag(models.Model):
    action_item = models.ForeignKey(ActionItem)
    user = models.ForeignKey(User)

class ActionItemVote(models.Model):
    action_item = models.ForeignKey(ActionItem)
    name = models.CharField(max_length=50)

class ActionItemInactive(models.Model):
    action_item = models.ForeignKey(ActionItem)
    reason = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

#reason - should be drop down -> duplicate, other, 