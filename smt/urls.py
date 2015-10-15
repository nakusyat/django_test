from django.conf.urls import patterns, url

from .views import IndexView
from .views import OpenFileView
from .views import DeleteFileView
from .views import TextAlignView
from .views import TokenizeView
from .views import Plain2SntView
from .views import WordClassesCoocView

urlpatterns = patterns('',
    url(r'^align/', TextAlignView.as_view(), name='align'),
    url(r'^tokenize/', TokenizeView.as_view(), name='tokenize'),
    url(r'^vcb/', Plain2SntView.as_view(), name='vcb'),
    url(r'^cooc/', WordClassesCoocView.as_view(), name='wc'),
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^(?P<file_name>.*)/$', OpenFileView.as_view(), name='open'),
    url(r'^(?P<file_name>.*)/delete$', DeleteFileView.as_view(), name='delete'),

)