from django.views.generic import View
from .tasks import scan_link
from sites_and_links.models import Link
from django.shortcuts import redirect


class ScanLinkView(View):
    def get(self, request, link_id, domain_id):
        scan_link(link_id)
        return redirect('admin_panel:show_domain', domain_id)
