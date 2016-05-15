from bs4 import BeautifulSoup
from urllib.request import urlopen

BASE_URL = 'http://wikilivres.ca/wiki/For_Whom_the_Bell_Tolls/'


def get_chapter(chapter_url):
    html = urlopen(chapter_url).read()
    soup = BeautifulSoup(html, 'lxml')
    chapter_text = soup.find('div', class_='text')
    return chapter_text

def replace_unicode_chars(text):
    ##might not be necessary
    return text


def get_book():
    for chapter in range(1, 44):
        print('Scraping chapter ' + str(chapter) + '...')
        chapter_url = BASE_URL + str(chapter)
        chapter_text = get_chapter(chapter_url)
        chapter_text = chapter_text.get_text()
        chapter_text = replace_unicode_chars(chapter_text)
        file = open('./text/chapter' + str(chapter), 'w')
        file.write(chapter_text)
        file.flush()

if __name__ == '__main__':
    get_book()