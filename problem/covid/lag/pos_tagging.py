#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path
from urllib.parse import urlparse
import os.path
import re

from html2text import html2text
import regex
import requests
import spacy
import typer


def _article_urls():
    return [
        ('https://www.nytimes.com/interactive/2022/07/07/us/ba5-covid-omicron-subvariant.html',
         'What the BA.5 Subvariant Could Mean for the United States'),
        ('https://www.nytimes.com/interactive/2021/us/covid-cases.html',
         'Coronavirus in the U.S.: Latest Map and Case Count'),
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
    skip_to_content_re = regex.compile(r'.*?<main id="site-content">')

    nlp = spacy.load('en_core_web_sm')  # $ python -m spacy download en_core_web_sm

    for url, title in _article_urls():
        html = _get_article_text(url)
        html = skip_to_content_re.sub('', html)
        print('\n\n====\n', url, title)

        doc = nlp(html2text(html))
        for ent in doc.ents:
            print(f'\n\n{ent.label_:<12} {ent.text}')


if __name__ == '__main__':
    typer.run(fetch_articles)
