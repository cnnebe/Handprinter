from django.test import TestCase
from .models import *
# Create your tests here.

class ProfileModelTest(TestCase):

	def test_roles(self):
		u1 = User.objects.create(username="joesmith", first_name="Joe", last_name="Smith", email="js@gmail.com")
		u2 = User.objects.create(username="admin", first_name="Joe", last_name="Smith", email="js@gmail.com")
		u3 = User.objects.create(username="mod", first_name="Joe", last_name="Smith", email="js@gmail.com")
		p1 = Profile.objects.create(user = u1)
		p2 = Profile.objects.create(user = u2, role = "admin")
		p3 = Profile.objects.create(user = u3, role = "moderator")
		self.assertEqual(p1.role, 'member')
		self.assertEqual(p2.role, "admin")
		self.assertEqual(p3.role, "moderator")

class ActionIdeaTest(TestCase):

	def test_str_repr(self):
		u1 = User.objects.create(username="joesmith", first_name="Joe", last_name="Smith", email="js@gmail.com")
		u2 = User.objects.create(username="admin", first_name="Joe", last_name="Smith", email="js@gmail.com")
		a1 = ActionIdea.objects.create(creator = u1, name = "Pump Tires", description = "Pump Tires increases air", category = "home")
		a2 = ActionIdea.objects.create(creator = u2, name = "Plant Trees", description = "Planting trees increase oxygen in the air", category = "home")
		self.assertEqual(str(a1), a1.name)
		self.assertEqual(str(a2), a2.name)

	def test_numvotes(self):
		u1 = User.objects.create(username="joesmith", first_name="Joe", last_name="Smith", email="js@gmail.com")
		u2 = User.objects.create(username="admin", first_name="Joe", last_name="Smith", email="js@gmail.com")
		u3 = User.objects.create(username="mod", first_name="Joe", last_name="Smith", email="js@gmail.com")
		a1 = ActionIdea.objects.create(creator = u1, name = "Pump Tires", description = "Pump Tires increases air", category = "home")
		self.assertEqual(a1.numvotes(), 0)		
		v1 = ActionIdeaVote.objects.create(action_idea = a1, user = u1)
		v2 = ActionIdeaVote.objects.create(action_idea = a1, user = u2)
		v3 = ActionIdeaVote.objects.create(action_idea= a1, user = u3)
		self.assertEqual(a1.numvotes(), 3)
		v3.delete()
		self.assertEqual(a1.numvotes(), 2)

	def test_comments(self):
		u1 = User.objects.create(username="joesmith", first_name="Joe", last_name="Smith", email="js@gmail.com")
		a1 = ActionIdea.objects.create(creator = u1, name = "Pump Tires", description = "Pump Tires increases air", category = "home")
		self.assertEqual(len(a1.comments()), 0)
		c1 = ActionIdeaComment(action_idea = a1, user = u1, text = "great idea!")
		c1.save()
		self.assertEqual(len(a1.comments()), 1)
		c1.delete()
		self.assertEqual(len(a1.comments()), 0)