from bs4 import BeautifulSoup


def get_title(html):
    soup = BeautifulSoup(html)
    title = soup.title.string.strip() if soup.title else ''
    return title


def get_description(html):
    soup = BeautifulSoup(html)
    description = soup.find(attrs={"name": "description"}).attrs['content'] if soup.find(
        attrs={"name": "description"}) else ''
    return description


def get_h1(html):
    soup = BeautifulSoup(html)
    h1 = soup.h1.string if soup.h1.string else ''
    return h1
