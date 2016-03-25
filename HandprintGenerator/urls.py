from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

app_name = 'HandprintGenerator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^handprintgenerator/(?P<actionidea_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_user$', views.new_user, name='new_user'),
    url(r'^new$', views.new_action_idea, name='new_action_idea'),
    url(r'^about$', TemplateView.as_view(template_name='about_us.html'), name="about_us"),
    url(r'^contact$', TemplateView.as_view(template_name='contact_us.html'), name="contact_us"),
    url(r'^privacy$', TemplateView.as_view(template_name='privacy_policy.html'), name="privacy_policy"),
    url(r'^terms$', TemplateView.as_view(template_name='terms_of_service.html'), name="terms_of_service"),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]