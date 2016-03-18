from django.conf.urls import url

from . import views

app_name = 'HandprintGenerator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^(?P<actionitem_id>[0-9]+)/$', views.detail, name='detail'),
  #  url(r'^create-user$', views.create_user),

	url(r'^new', views.new_action_item, name='new_action_item'),
	url(r'^register', views.new_user, name='register'),
	url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about'),
    url(r'^privacy-policy/$', views.flatpage, {'url': '/privacy-policy/'}, name='privacy')
    url(r'^contact-us/$', views.flatpage, {'url': '/contact-us/'}, name='contact'),

]