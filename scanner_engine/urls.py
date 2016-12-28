from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^scan_link/([0-9]+)/([0-9]+)/$', views.ScanLinkView.as_view(), name='scan_link'),
]
