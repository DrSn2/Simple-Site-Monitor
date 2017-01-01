from celery import task
from sites_and_links.models import Link
from .models import LinkScan
from .utils import get_title, get_description, get_h1, find_custom_code
import requests


@task()
def scan_all_links():
    links = Link.objects.all()
    for link in links:
        scan_link(link.id)


@task()
def scan_link(link_id):
    # Get link from the DB
    link = Link.objects.get(id=link_id)

    # Crawl given link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    try:
        response = requests.get(
            link.get_full_address(),
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        return False

    # Get data from the response content and save scan to the DB
    scan_result = LinkScan()
    scan_result.link = link
    scan_result.title = get_title(response.content)
    scan_result.description = get_description(response.content)
    scan_result.h1 = get_h1(response.content)

    # Look for custom code if necessary
    if link.custom_code != '':
        scan_result.contains_custom_code = find_custom_code(response.content, link.custom_code)

    scan_result.save()

    return True
