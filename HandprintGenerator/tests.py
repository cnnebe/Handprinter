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
