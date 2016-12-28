from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [

    # Default redirect to the login
    url(r'^$', RedirectView.as_view(url='login/', permanent=False), name='index'),

    # Authentication
    url(r'^login/$', views.Login.as_view(), name='client_login'),
    url(r'^logout/$', views.Logout.as_view(), name='client_logout')
]
