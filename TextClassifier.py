from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import csv
from names_dataset import NameDataset


class TextClassifier:

    """
    param categories: the list of categories into which to classify text
    param keywords: the 2D list of keywords for each category
    """
    def __init__(self, categories, keywords):
        self.training = []
        self.categories = categories
        self.training = TextClassifier.fetch_training_data(keywords)
        # get training data:
        # pull from google search of short list of terms for category
        # strip most common words -> list of training words for category

    @staticmethod
    def fetch_urls(keywords, n):
        urls = []
        for k in keywords:
            url_gen = search(k, stop=n)
            for url in url_gen:
                urls.append(url)
        print('fetched urls')
        return urls

    @staticmethod
    def tag_body_text(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[Document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    @staticmethod
    def scrape_text(url):
        try:
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers = {'User-Agent': user_agent}

            req = Request(url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, features='html.parser')
            try:
                h1 = soup.body.find('h1')  # find the common parent for <h1> and all <p>s.
                root = h1
                while root.name != 'body' and len(root.find_all('p')) < 5:
                    root = root.parent
                # find all the content elements.
                ps = root.find_all(['p', 'pre'])
                text = [p.text for p in ps]
            except AttributeError:
                for s in soup(['script', 'style']):
                     s.extract()

                text = soup.body.getText()

            lines = [line.strip() for p in text for line in p.splitlines() if len(p) > 10]
            words = [word.strip() for line in lines for word in line.split(' ')]
            text = [word for word in words if word]

            print('scraped text')
            return text

        except (TimeoutError, HTTPError):
            return []

    @staticmethod
    def read_frequent_words():
        frequent_words = []
        with open('data/frequentwords.csv') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                frequent_words.append(row[1].strip())
        frequent_words = frequent_words[0:100]
        frequent_words.extend(['all', 'rights', 'reserved', 'photo', 'by:'])
        print('read frequent')
        return frequent_words

    @staticmethod
    def read_frequent_names():
        frequent_names = []
        with open('data/new-top-surnames.csv') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                frequent_names.append(row[1].strip().lower())
        with open('data/new-top-firstNames.csv') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                frequent_names.append(row[1].strip().lower())
        return frequent_names

    @staticmethod
    def fetch_training_data(keywords):

        frequent = TextClassifier.read_frequent_words()
        nd = NameDataset()
        #frequent.extend(TextClassifier.read_frequent_names())

        # k is a list of keywords for a specific category
        training = []
        for k in keywords:
            urls = TextClassifier.fetch_urls(k, 10)
            text = []
            for url in urls:
                text.extend(TextClassifier.scrape_text(url))
            text = [t.lower() for t in text
                    if t.lower() not in frequent
                    and not nd.search_first_name(t)
                    and not nd.search_last_name(t)]
            print(text[0:100])
            print(len(text))
            training.append(text)
        return training


if __name__ == '__main__':
    tc = TextClassifier(['Food'],
                        [['dinner', 'restaurants near me', 'restaurants',
                          'go out to eat', 'food', 'cuisines', 'groceries']])
