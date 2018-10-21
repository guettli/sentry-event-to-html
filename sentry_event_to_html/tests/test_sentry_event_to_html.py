# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import io
import sys
import tempfile
import unittest
import webbrowser

from sentry_sdk.utils import event_from_exception

import sentry_event_to_html

class TestCase(unittest.TestCase):

    def create_event(self):
        try:
            local_var = 'foo'
            return self.some_sub_method()
        except Exception as exc:
            event, info = event_from_exception(sys.exc_info(), with_locals=True)
            return event

    def some_sub_method(self):
        local_var = 'bar'
        raise ValueError()

    def test_sentry_event_to_html(self):
        html=sentry_event_to_html.sentry_event_to_html(self.create_event())
        temp_html = tempfile.mktemp(prefix='test_sentry_event_to_html', suffix='.html')
        with io.open(temp_html, 'wt', encoding='utf8') as fd:
            fd.write('''<html>
             <head>{}</head>
            <body>
            {}
            </body>
            </html>'''.format(sentry_event_to_html.html_head(), html))
        webbrowser.open(temp_html)