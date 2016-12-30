from bs4 import BeautifulSoup


def get_title(html):
    soup = BeautifulSoup(html)
    title = soup.title
    title = title.string.strip() if title else ''
    return title


def get_description(html):
    soup = BeautifulSoup(html)
    description = soup.find(attrs={"name": "description"})
    description = description.attrs['content'] if description else ''
    return description


def get_h1(html):
    soup = BeautifulSoup(html)
    h1 = soup.find('h1')
    h1 = h1.string.strip() if h1 else ''
    return h1
