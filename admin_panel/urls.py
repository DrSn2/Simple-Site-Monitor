from django.conf.urls import url
from . import views

urlpatterns = [
    # Index
    url(r'^$', views.ListDomains.as_view(), name='panel'),
    # Domains
    url(r'^add_domain/$', views.AddDomain.as_view(), name='add_domain'),
    url(r'^add_link/([0-9]+)/$', views.AddLink.as_view(), name='add_link'),
    url(r'^show_domain/([0-9]+)/$', views.ShowDomain.as_view(), name='show_domain'),
    url(r'^show_link/([0-9]+)/$', views.ShowLink.as_view(), name='show_link'),
    url(r'^delete_domain/([0-9]+)/$', views.DeleteDomain.as_view(), name='delete_domain'),
]
