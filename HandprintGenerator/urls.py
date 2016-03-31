from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views
from django.views.generic import TemplateView

app_name = 'HandprintGenerator'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index$', views.index, name='index'),
    url(r'^create_user$', views.new_user, name='new_user'),
    url(r'^profile$', views.user_profile, name='user_profile'),
    url(r'^new$', views.edit_action_idea, name='new_action_idea'),
    url(r'^handprintgenerator/(?P<actionidea_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^handprintgenerator/(?P<actionidea_id>[0-9]+)/edit/$', views.edit_action_idea, name='edit_action_idea'),
    url(r'^handprintgenerator/(?P<actionidea_id>[0-9]+)/delete/$', views.delete_action_idea, name='delete_action_idea'),
    url(r'^about$', TemplateView.as_view(template_name='about_us.html'), name="about_us"),
    url(r'^contact$', TemplateView.as_view(template_name='contact_us.html'), name="contact_us"),
    url(r'^privacy$', TemplateView.as_view(template_name='privacy_policy.html'), name="privacy_policy"),
    url(r'^terms$', TemplateView.as_view(template_name='terms_of_service.html'), name="terms_of_service"),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]
