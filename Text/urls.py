from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.homeIndex,name='homeIndex'),
    url(r'^TextPsyche/',views.homeIndex,name='homeIndex'),
    url(r'^analyze/',views.get_text,name='get_text'),
    url(r'^fileprocess/',views.upload_file,name='upload_file'),
    url(r'^Download/',views.download_option,name='download_option'),
    url(r'^snippets/$', views.api_Data_process),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.api_Data_process)
    #url(r'^charts/$', views.chart, name = 'demo'),
    #url(r'^charttry/$', views.charttry, name = 'demo')
   
]


urlpatterns = format_suffix_patterns(urlpatterns)
