from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # Domain shouldn't have www and http/https
    domain = models.CharField(null=False, blank=False, max_length=250,
                              validators=[RegexValidator(
                                  regex='^(?!www.|http:\/\/|https\/\/)',
                                  message='Domain cannot have www nad http/https',
                                  code='invalid_address'
                              )])
    https = models.BooleanField(blank=True, default=False)
    www = models.BooleanField(blank=True, default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.domain

    def get_domain_address(self):
        domain_name = self.domain
        if self.www:
            domain_name = 'www.' + domain_name
        if self.https:
            domain_name = 'https://' + domain_name
        else:
            domain_name = 'http://' + domain_name
        return domain_name


class Link(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=False)
    # Address should start with /
    address = models.CharField(null=False, blank=False, default='/', max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    title = models.CharField(null=True, blank=True, default='', max_length=400)
    description = models.CharField(null=True, blank=True, default='', max_length=500)
    h1 = models.CharField(null=True, blank=True, default='', max_length=200)
    custom_code = models.TextField(null=True, blank=True, default='', max_length=3000)

    def __unicode__(self):
        return self.domain.get_domain_address() + self.address

    def get_full_address(self):
        return self.domain.get_domain_address() + self.address
