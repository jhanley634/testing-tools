#! /usr/bin/env python
from bs4 import BeautifulSoup
from html2text import html2text
import spacy
import typer

from problem.covid.lag.pos_tagging import _get_article_text


class NewsArticle:

    def __init__(self, url):
        self.nlp = spacy.load('en_core_web_sm')
        self.html = _get_article_text(url)
        self.doc = self.nlp(html2text(self.html))

    def _get_paragraphs(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        for p in soup.find_all('p'):
            yield p.text

    def get_sentences(self):
        for para in self._get_paragraphs():
            yield from para.split('.')


def main(url: str):
    assert url.startswith('https://www.theguardian.com'), url
    for i, s in enumerate(NewsArticle(url).get_sentences()):
        print(i, s)


if __name__ == '__main__':
    typer.run(main)
