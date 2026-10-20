"""Regression tests for the single-page countdown content and schema repair."""
import copy
import html
import json
import re
import unittest
from unittest.mock import patch

import build_banner_snapshot as build


class CountdownSEOTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads(build.DATA_JSON.read_text())
        self.original = build.COUNTDOWN_HTML.read_text()

    def test_current_deadline_uses_original_clock_and_timezone(self):
        text = build.render_countdown_page(self.original, self.snapshot)
        self.assertIn('October 22, 2026 at 09:59 (server time)', text)
        self.assertIn('not a live seconds-remaining timer', text)
        self.assertNotIn('query variants that are already getting impressions', text)

    def test_schema_matches_visible_faq_exactly(self):
        text = build.render_countdown_page(self.original, self.snapshot)
        payload = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])
        faq = next(x for x in payload['@graph'] if x['@type'] == 'FAQPage')
        visible = [(html.unescape(q), html.unescape(a)) for q, a in re.findall(r'<article class="faq-item"><h3>(.*?)</h3><p>(.*?)</p></article>', text)]
        encoded = [(x['name'], x['acceptedAnswer']['text']) for x in faq['mainEntity']]
        self.assertEqual(encoded, visible)
        self.assertEqual(len(encoded), 4)

    def test_title_meta_canonical_and_h1_are_unchanged(self):
        text = build.render_countdown_page(self.original, self.snapshot)
        for pattern in [r'<title>.*?</title>', r'<meta [^>]+>', r'<link rel="canonical"[^>]+>', r'<h1>.*?</h1>']:
            self.assertEqual(re.findall(pattern, text), re.findall(pattern, self.original))

    def test_no_fake_source_verification_date(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot['updated'] = '2026-10-20'
        text = build.build_countdown_sources(snapshot)
        self.assertIn('Source record last verified: 2026-10-01', text)
        self.assertIn('Rebuilding this page does not re-verify the source', text)

    def test_render_is_idempotent(self):
        once = build.render_countdown_page(self.original, self.snapshot)
        self.assertEqual(once, build.render_countdown_page(once, self.snapshot))

    def test_pending_next_does_not_invent_date(self):
        text = build.render_countdown_page(self.original, self.snapshot)
        self.assertIn('The next post-current banner date is not official yet', text)
        self.assertIn('Not announced yet', text)

    def test_future_phase_uses_new_values_not_hardcoded_current(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot['current']['end_date'] = '2026-11-12 23:59'
        snapshot['current']['featured_characters'] = ['Example Resonator']
        text = build.render_countdown_page(self.original, snapshot)
        self.assertIn('November 12, 2026 at 23:59 (server time)', text)
        self.assertIn('When does the Example Resonator banner end?', text)
        self.assertNotIn('October 22, 2026 at 09:59', text)

    def test_missing_timezone_does_not_assume_utc_offset(self):
        with patch.object(build, 'load_rows', return_value=[]):
            deadline = build.countdown_deadline(self.snapshot['current'])
        self.assertIn('timezone not specified', deadline)
        self.assertNotIn('UTC', deadline)


if __name__ == '__main__':
    unittest.main()
