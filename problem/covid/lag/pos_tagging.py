#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path
from urllib.parse import urlparse
import os.path
import re

from bs4 import BeautifulSoup
from html2text import html2text
import requests
import spacy
import typer


def article_urls():
    return [
        ('https://www.nytimes.com/interactive/2022/07/07/us/ba5-covid-omicron-subvariant.html',
         'What the BA.5 Subvariant Could Mean for the United States'),
        ('https://www.nytimes.com/interactive/2021/us/covid-cases.html',
         ''),
    ]


def _get_article_text(url):
    fspec = _get_fspec(url)
    if not fspec.exists():
        r = requests.get(url)
        r.raise_for_status()
        assert 'ad blocker' not in r.text, r.text
        with open(fspec, 'w') as fout:
            fout.write(r.text)
    with open(fspec) as fin:
        return fin.read()


def _get_fspec(url, folder='/tmp'):
    p = urlparse(url)
    name = os.path.basename(p.path)
    sane_re = re.compile(r'^[\w.-]+$')
    assert sane_re.search(name), name
    return Path(f'{folder}/{name}')


def fetch_articles():
    skip_to_content_re = re.compile(r'.*<main id="site-content">')

    nlp = spacy.load('en_core_web_sm')  # $ python -m spacy download en_core_web_sm

    for url, title in article_urls():
        html = skip_to_content_re.sub('<p>hi there!</p>', _get_article_text(url))
        soup = BeautifulSoup(html, 'html.parser')
        print('\n\n====\n', url, title, html2text(soup.prettify()))

        doc = nlp(html2text(soup.prettify()))
        for ent in doc.ents:
            print(ent)
            print(ent.label_, ent.text)


if __name__ == '__main__':
    typer.run(fetch_articles)
