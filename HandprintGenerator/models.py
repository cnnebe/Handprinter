from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

class ActionItem(models.Model):
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    links = models.CharField(max_length=500)
    images = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    #datecreated = models.DateTimeField(auto_now_add=True, blank=True)

class ActionItemComment(models.Model):
    action_item = models.ForeignKey(ActionItem)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)

class ActionItemTag(models.Model):
    action_item = models.ForeignKey(ActionItem)
    user = models.ForeignKey(User)

class ActionItemVote(models.Model):
    action_item = models.ForeignKey(ActionItem)
    name = models.CharField(max_length=50)

class ActionItemInactive(models.Model):
    action_item = models.ForeignKey(ActionItem)
    reason = models.CharField(max_length=150)

#reason - should be drop down -> duplicate, other, 