#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
import unittest

import typer


class NewsTest(unittest.TestCase):

    def test_news(self):
        self.assertTrue(True)


def main():
    ''


if __name__ == '__main__':
    unittest.main()
    typer.run(main)
