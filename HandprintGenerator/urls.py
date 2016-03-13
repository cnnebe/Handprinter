from django.conf.urls import url

from . import views

app_name = 'HandprintGenerator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^(?P<actionitem_id>[0-9]+)/$', views.detail, name='detail'),
  #  url(r'^create-user$', views.create_user),

	#url(r'^new', views.new_action_item, name='new_action_item'),

]