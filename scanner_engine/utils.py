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
    h1 = h1.get_text() if h1 else ''
    h1 = "".join(h1.split())
    return h1


def find_custom_code(html, custom_code):
    # Remove white spaces and lower
    html = "".join(html.split())
    custom_code = "".join(custom_code.split())
    html = html.lower()
    custom_code = custom_code.lower()

    if custom_code in html:
        return True
    else:
        return False
