from django.conf.urls import url

from . import views

app_name = 'HandprintGenerator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
	url(r'^(?P<actionitem_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_user', views.new_user, name='new_user'),
	url(r'^new', views.new_action_item, name='new_action_item'),
    url(r'^users', views.user_index, name='user_index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
]