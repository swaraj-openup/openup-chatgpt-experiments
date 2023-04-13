from googleapiclient.discovery import build
import pprint
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

my_api_key = ""
my_cse_id = ""


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    # texts = soup.div['class']
    # texts = soup.find_all("div", class_="c-post-text__content-box").split("\n")
    # print(texts)
    # texts = soup.findAll("div", {"class": "c-post-text__content-box"})
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search(
    '" Annemarie Andre " site:https://openup.com/blog/', my_api_key, my_cse_id, num=10)
for result in results:
    html = urllib.request.urlopen(result['link']).read()
    print(text_from_html(html))
    break