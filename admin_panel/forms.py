from django import forms
from sites_and_links.models import Domain, Link


class AddDomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['domain', 'https', 'www']


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['address', 'title', 'description', 'h1', 'custom_code']
