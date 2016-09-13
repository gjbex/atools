#!/usr/bin/env python

import unittest


class TestLogParser(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.log_parser'''

    def test_(self):
        from vsc.atools.log_parser import LogEvent, InvalidLogEntryError
        event_str = 'bla bla bla'
        try:
            _ = LogEvent.parse_str(event_str)
            self.assertTrue(False)
        except InvalidLogEntryError:
            pass


if __name__ == '__main__':
    unittest.main()
