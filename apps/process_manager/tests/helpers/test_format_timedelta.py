import unittest
from datetime import timedelta

from process_manager.helpers.format_timedelta import format_timedelta


class TestFormatTimedelta(unittest.TestCase):
    def test_format_timedelta(self):
        td = timedelta(days=1, hours=2, minutes=30)
        formatted = format_timedelta(td)
        self.assertEqual(formatted, "1d 2h 30m")

        td = timedelta(days=0, hours=0, minutes=0)
        formatted = format_timedelta(td)
        self.assertEqual(formatted, "0d 0h 0m")

        td = timedelta(days=5, hours=23, minutes=59)
        formatted = format_timedelta(td)
        self.assertEqual(formatted, "5d 23h 59m")
