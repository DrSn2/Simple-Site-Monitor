from __future__ import unicode_literals
from django.db import models
from sites_and_links.models import Link


class LinkScan(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, null=False)
    title = models.CharField(null=False, blank=True, default='', max_length=400)
    description = models.CharField(null=False, blank=True, default='', max_length=500)
    h1 = models.CharField(null=False, blank=True, default='', max_length=200)
    contains_custom_code = models.BooleanField(blank=True, default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '{} - {}'.format(self.link.get_full_address(), self.timestamp)

    # Check if data from scan matches desired data for this link
    def title_is_correct(self):
        return self.title == self.link.title

    def description_is_correct(self):
        return self.description == self.link.description

    def h1_is_correct(self):
        return self.h1 == self.link.h1

    def everything_is_correct(self):
        return self.title == self.link.title and self.description == self.link.description and self.h1 == self.link.h1 and self.contains_custom_code
