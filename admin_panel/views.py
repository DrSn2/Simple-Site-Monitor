from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from sites_and_links.models import Domain, Link
from .forms import AddDomainForm, AddLinkForm
from scanner_engine.tasks import scan_link
from scanner_engine.models import LinkScan


# Display list of domains and links
@method_decorator(login_required, name='dispatch')
class ListDomains(View):
    template_name = 'admin_panel/dashboard.html'

    def get(self, request):
        sites_and_links = []

        for domain in Domain.objects.all():
            links = Link.objects.filter(domain=domain)
            scans = []
            for link in links:
                # Get newest scan for every link
                scan = LinkScan.objects.filter(link=link).order_by('-id')[0]
                # Create flag for the template
                flag = scan.everything_is_correct()
                scan.is_correct = flag
                scans.append(scan)
            sites_and_links.append({
                'domain': domain,
                'scans': scans
            })

        return render(request, self.template_name, {
            'sites_and_links': sites_and_links
        })


# Add new domain
@method_decorator(login_required, name='dispatch')
class AddDomain(View):
    template_name = 'admin_panel/add_domain.html'

    def get(self, request):
        add_domain_form = AddDomainForm()
        return render(request, self.template_name, {'form': add_domain_form})

    def post(self, request):
        context = {
            'form': None,
            'message': None,
            'message_class': None
        }
        form = AddDomainForm(request.POST)
        new_domain = None

        try:
            if form.is_valid():
                # Register new domain
                new_domain = form.save(commit=False)
                new_domain.user = request.user
                # Delete trailing slash from the domain name
                if new_domain.domain[-1] == '/':
                    new_domain.domain = new_domain.domain[:-1]
                new_domain.save()

                # Create root link for the new domain
                root_link = Link()
                root_link.domain = new_domain
                root_link.address = '/'
                root_link.save()
                # Scan root link and delete new domain if scanning is impossible
                if not scan_link(root_link.id):
                    new_domain.delete()
                    context['message'] = 'Cannot scan given domain'
                    context['message_class'] = 'alert-danger'
                    context['form'] = form
                else:
                    context['message'] = 'New domain added!'
                    context['message_class'] = 'alert-success'
                    context['form'] = AddDomainForm(None)

            else:
                context['message'] = 'Invalid domain!'
                context['message_class'] = 'alert-danger'
                context['form'] = form

        except Exception as e:
            print e
            # Delete new domain if error occurred
            if new_domain:
                new_domain.delete()
            context['message'] = 'Unexpected error occurred!'
            context['message_class'] = 'alert-danger'
            context['form'] = form

        return render(request, self.template_name, context)


# Add new link for the given domain
@method_decorator(login_required, name='dispatch')
class AddLink(View):
    template_name = 'admin_panel/add_link.html'

    def get(self, request, domain_id):
        # Get parent domain
        parent_domain = Domain.objects.get(id=domain_id)

        add_link_form = AddLinkForm()
        return render(request, self.template_name, {
            'form': add_link_form,
            'domain': parent_domain
        })

    def post(self, request, domain_id):
        # Get parent domain
        parent_domain = Domain.objects.get(id=domain_id)

        context = {
            'form': None,
            'message': None,
            'message_class': None,
            'domain': parent_domain
        }
        form = AddLinkForm(request.POST)

        try:
            if form.is_valid():
                # Register new link for the domain
                new_link = form.save(commit=False)
                new_link.domain = parent_domain
                new_link.save()
                # Scan registered link
                scan_link(new_link.id)

                context['message'] = 'New link added!'
                context['message_class'] = 'alert-success'
                context['form'] = AddLinkForm(None)

            else:
                context['message'] = 'Invalid data!'
                context['message_class'] = 'alert-danger'
                context['form'] = form

        except Exception:
            context['message'] = 'Unexpected error occurred!'
            context['message_class'] = 'alert-danger'
            context['form'] = form

        return render(request, self.template_name, context)


# Show and edit domain
@method_decorator(login_required, name='dispatch')
class ShowDomain(View):
    template_name = 'admin_panel/show_domain.html'

    def get(self, request, domain_id):
        parent_domain = Domain.objects.get(id=domain_id)

        links = Link.objects.filter(domain=parent_domain)
        scans = []
        for link in links:
            # Get newest scan for every link
            scan = LinkScan.objects.filter(link=link).order_by('-id')[0]
            # Create flags for the template
            scan.title_is_correct = scan.title_is_correct()
            scan.description_is_correct = scan.description_is_correct()
            scan.h1_is_correct = scan.h1_is_correct()
            scan.custom_code_is_correct = scan.contains_custom_code
            scans.append(scan)

        form = AddDomainForm(instance=parent_domain)

        return render(request, self.template_name, {
            'domain': parent_domain,
            'scans': scans,
            'form': form
        })

    def post(self, request, domain_id):
        # Get domain and list of scans
        parent_domain = Domain.objects.get(id=domain_id)
        links = Link.objects.filter(domain=parent_domain)
        scans = []
        for link in links:
            # Get newest scan for every link
            scan = LinkScan.objects.filter(link=link).order_by('-id')[0]
            # Create flags for the template
            scan.title_is_correct = scan.title_is_correct()
            scan.description_is_correct = scan.description_is_correct()
            scan.h1_is_correct = scan.h1_is_correct()
            scans.append(scan)

        context = {
            'form': None,
            'message': None,
            'message_class': None,
            'scans': scans,
            'domain': parent_domain
        }

        # Assign desired domain to the form
        form = AddDomainForm(request.POST, instance=parent_domain)

        try:
            if form.is_valid():
                # Save changes from form
                form.save()

                context['message'] = 'Success!'
                context['message_class'] = 'alert-success'
                context['form'] = form

            else:
                context['message'] = 'Invalid domain!'
                context['message_class'] = 'alert-danger'
                context['form'] = form

        except Exception:
            context['message'] = 'Unexpected error occurred!'
            context['message_class'] = 'alert-danger'
            context['form'] = form

        return render(request, self.template_name, context)


# Show and edit specific link for the given domain
@method_decorator(login_required, name='dispatch')
class ShowLink(View):
    template_name = 'admin_panel/show_link.html'

    def setup_flags(self, scan):
        title_class = 'panel-success' if scan.title_is_correct() else 'panel-danger'
        description_class = 'panel-success' if scan.description_is_correct() else 'panel-danger'
        h1_class = 'panel-success' if scan.h1_is_correct() else 'panel-danger'
        return title_class, description_class, h1_class

    def get(self, request, link_id):
        # Get link from DB and display into form
        link = Link.objects.get(id=link_id)
        scan = LinkScan.objects.filter(link=link).order_by('-id')[0]
        form = AddLinkForm(instance=link)

        # Set flags for the template
        (title_class, description_class, h1_class) = self.setup_flags(scan)

        return render(request, self.template_name, {
            'link': link,
            'scan': scan,
            'domain': link.domain,
            'form': form,
            'title_class': title_class,
            'description_class': description_class,
            'h1_class': h1_class
        })

    def post(self, request, link_id):
        # Get link from DB and display into form
        link = Link.objects.get(id=link_id)
        # Get latest scan from the DB
        scan = LinkScan.objects.filter(link=link).order_by('-id')[0]

        # Set flags for the template
        (title_class, description_class, h1_class) = self.setup_flags(scan)

        context = {
            'form': None,
            'message': None,
            'message_class': None,
            'link': link,
            'scan': scan,
            'domain': link.domain,
            'title_class': title_class,
            'description_class': description_class,
            'h1_class': h1_class
        }

        # Assign desired link to the form
        form = AddLinkForm(request.POST, instance=link)

        try:
            if form.is_valid():
                # Save changes from form
                form.save()

                context['message'] = 'Success!'
                context['message_class'] = 'alert-success'
                context['form'] = form

            else:
                context['message'] = 'Invalid data!'
                context['message_class'] = 'alert-danger'
                context['form'] = form

        except Exception:
            context['message'] = 'Unexpected error occurred!'
            context['message_class'] = 'alert-danger'
            context['form'] = form

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class DeleteDomain(View):

    def get(self, request, domain_id):
        domain = Domain.objects.get(id=domain_id)
        domain.delete()

        return redirect('admin_panel:panel')
