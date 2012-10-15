from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('gov_inspector.views',
    (r'^$', 'index'),
    (r'^ministries/$', 'ministries'),
    #('^humans.txt$', redirect_to, {'url': '/static/humans.txt'}),
)
