import requests
from bs4 import BeautifulSoup
from time import sleep

from app import db
from app.models import Post


class Parser:
    """The base class of website parsers"""

    def __init__(self, base_url):
        self.base_url = base_url

    def get_html(self):
        """Returns the html text"""
        return requests.get(self.base_url).text

    def get_soup(self):
        """Returns a BeautifulSoup class object"""
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def save_data(self, data):
        source = data['source']
        title = data['title']
        url = data['link']

        if len(Post.query.filter_by(url=url).all()) == 0:
            post = Post(title, url)
            post.source = source

            db.session.add(post)
            db.session.commit()


def parse_raywenderlich():
    """The RayWenderlich.com website parsing"""
    source = 'RayWenderlich'
    url = 'https://www.raywenderlich.com'
    parser = Parser(base_url=url)

    soup = parser.get_soup()
    articles = soup.find_all('article', class_='post')

    for article in articles:
        title = article.find('h2').text.strip()
        link = article.find('h2').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        if 'iOS' in title or 'Swift' in title:
            data = {'source': source, 'title': title, 'link': link}
            parser.save_data(data)


def parse_appcoda():
    """The AppCoda.com website parsing"""
    source = 'AppCoda'
    url = 'http://www.appcoda.com/'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('article', class_='post')

    for article in articles:
        title = article.find('div', class_='post-content').find('h2').text.strip()
        link = article.find('div', class_='post-content').find('h2').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def parse_nsscreencast():
    """The NSScreenсast.com website parsing"""
    source = 'NSScreencast'
    url = 'http://nsscreencast.com/episodes/free#episodes'

    base_url = 'http://nsscreencast.com'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find('div', class_='episodes').find_all('div', class_='col-sm-6')

    for article in articles:
        title = article.find('div', class_='episode_info').find('a', class_='episode__title').text.strip()
        link = article.find('div', class_='episode_info').find('a', class_='episode__title').get('href').strip()
        link = base_url + link

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def parse_codementor():
    """The Codementor.com website parsing"""
    source = 'Codementor'
    url = 'https://www.codementor.io/community/topic/swift'

    base_url = 'https://www.codementor.io'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('div', class_='community-post')

    for article in articles:
        title = article.find('h3', class_='community-post__title').text.strip()
        link = base_url + article.find('div', class_='community-post__body').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def parse_codingexplorer():
    """The CodingExplorer.com website parsing"""
    source = 'The Coding Explorer Blog'
    url = 'http://www.codingexplorer.com/'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('article', class_='post')

    for article in articles:
        title = article.find('h2', class_='entry-title').text.strip()
        link = article.find('h2', class_='entry-title').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def parse_objc():
    """The objc.io website parsing"""
    source = 'objc.io'
    url = 'https://talk.objc.io/'

    base_url = 'https://talk.objc.io'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('div', class_='episode-cell')

    for article in articles:
        if article.find('p', class_='color-blue') is None:
            title = article.find('span', class_='color-blue').text.strip()
            link = article.find('a', class_='block').get('href').strip()
            link = base_url + link

            if title is None:
                title = ''
            if link is None:
                link = ''

            data = {'source': source, 'title': title, 'link': link}
            parser.save_data(data)


def parse_maniacdev():
    """The ManiacDev.com website parsing"""
    source = 'ManiacDev'
    url = 'https://maniacdev.com/category/ios-developer-tutorial/'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('div', class_='post')

    for article in articles:
        title = article.find('h2', class_='art-postheader').find('a').text.strip()
        link = article.find('h2', class_='art-postheader').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def parse_natashatherobot():
    """The NatashaTheRobot.com website parsing"""
    source = 'NatashaTheRobot.com'
    url = 'https://www.natashatherobot.com/'

    parser = Parser(base_url=url)
    soup = parser.get_soup()

    articles = soup.find_all('article', class_='blog-teaser')

    for article in articles:
        title = article.find('h2').find('a').text.strip()
        link = article.find('h2').find('a').get('href').strip()

        if title is None:
            title = ''
        if link is None:
            link = ''

        data = {'source': source, 'title': title, 'link': link}
        parser.save_data(data)


def run_parsing():
    while True:
        parse_raywenderlich()
        parse_appcoda()
        parse_nsscreencast()
        parse_codementor()
        parse_codingexplorer()
        parse_objc()
        parse_maniacdev()
        parse_natashatherobot()

        # Run twice a day (every 12 hours)
        sleep(12 * 60 * 60)


def parse_all():
    parse_raywenderlich()
    parse_appcoda()
    parse_nsscreencast()
    parse_codementor()
    parse_codingexplorer()
    parse_objc()
    parse_maniacdev()
    parse_natashatherobot()
