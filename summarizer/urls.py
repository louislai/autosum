from django.conf.urls import patterns, include, url
from django.contrib import admin
from analyzer import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'summarizer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^cluster', views.cluster),
    url(r'^compare', views.compare),
    url(r'^$', views.index),
    url(r'^summarize$', views.summarize),
    url(r'^index', views.index),
    url(r'^admin/', include(admin.site.urls)),
)
