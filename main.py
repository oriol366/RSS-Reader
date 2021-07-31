from os import read
import feedparser
from feedparser.api import parse
import timg
import requests
from io import BytesIO
from bs4 import BeautifulSoup


def ask_url():
    return input("Please, Enter an RSS feed URL: ")

def parse_url(url):
    d = feedparser.parse(url)
    if 'title' in d.feed:
        return d
    else:
        print("URL not valid")
        return parse_url(ask_url())

def print_image(image_url):
    i = timg.Renderer()
    i.load_image_from_file(BytesIO(requests.get(image_url).content))
    i.resize(100,40)
    i.render(timg.ASCIIMethod)

def read_RSS(s):
    entry = 0
    while True:
        print("Title: ", s.entries[entry].title)
        soup = BeautifulSoup(s.entries[entry].summary, 'html.parser')
        for link in soup.find_all('img', limit=1):
            print_image(link.get('src'))
        print(soup.get_text())

        i = input("Choose option: [p->prev | n->next | q->quit | e->exit]: ")
        if i == 'p' and entry > 0:
            entry -= 1
        elif i == 'n' and len(s.entries) > (entry+1):
            entry += 1
        elif i == 'q':
            break
        else:
            exit()

def main():
    url = ask_url()
    while url:
        d = parse_url(url)
        print_image(d.feed.image.href)
        print("Do you want to read RSS from {}".format(d.feed.title))
        r = input("[Y/n]?")
        if r == 'n':
            url = ask_url()
            pass
        read_RSS(d)



if __name__ == "__main__":
    main()