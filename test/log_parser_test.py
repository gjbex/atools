#!/usr/bin/env python

from datetime import datetime
import math
import unittest


class TestLogParser(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.log_parser'''

    def test_invalid_event(self):
        from vsc.atools.log_parser import LogEvent, InvalidLogEntryError
        event_str = 'bla bla bla'
        try:
            _ = LogEvent.parse_str(event_str)
            self.assertTrue(False)
        except InvalidLogEntryError:
            pass

    def test_invalid_event_type(self):
        from vsc.atools.log_parser import LogEvent, InvalidLogEventError
        event_str = '4 flabbered by r1i1n3 at 2016-09-02 11:47:46'
        try:
            _ = LogEvent.parse_str(event_str)
            self.assertTrue(False)
        except InvalidLogEventError:
            pass

    def test_start_event(self):
        from vsc.atools.log_parser import LogEvent
        expected_type = 'started'
        expected_item_id = 4
        expected_slave_id = 'r1i1n3'
        expected_time = datetime(2016, 9, 2, 11, 47, 46 )
        event_str = '4 started by r1i1n3 at 2016-09-02 11:47:46'
        event = LogEvent.parse_str(event_str)
        self.assertEquals(expected_type, event.type)
        self.assertEquals(expected_item_id, event.item_id)
        self.assertEquals(expected_slave_id, event.slave_id)
        self.assertEquals(expected_time, event.time_stamp)
        
    def test_failed_event(self):
        from vsc.atools.log_parser import LogEvent
        expected_type = 'failed'
        expected_item_id = 5
        expected_slave_id = 'r1i1n3'
        expected_time = datetime(2016, 9, 2, 11, 47, 47 )
        expected_exit_status = 1
        event_str = '5 failed by r1i1n3 at 2016-09-02 11:47:47: 1'
        event = LogEvent.parse_str(event_str)
        self.assertEquals(expected_type, event.type)
        self.assertEquals(expected_item_id, event.item_id)
        self.assertEquals(expected_slave_id, event.slave_id)
        self.assertEquals(expected_time, event.time_stamp)
        self.assertEquals(expected_exit_status, event.exit_status)

    def test_completed_event(self):
        from vsc.atools.log_parser import LogEvent
        expected_type = 'completed'
        expected_item_id = 10
        expected_slave_id = 'r1i1n3'
        expected_time = datetime(2016, 9, 2, 11, 47, 53 )
        expected_exit_status = 0
        event_str = '10 completed by r1i1n3 at 2016-09-02 11:47:53'
        event = LogEvent.parse_str(event_str)
        self.assertEquals(expected_type, event.type)
        self.assertEquals(expected_item_id, event.item_id)
        self.assertEquals(expected_slave_id, event.slave_id)
        self.assertEquals(expected_time, event.time_stamp)
        self.assertEquals(expected_exit_status, event.exit_status)

    def test_parse_file(self):
        from vsc.atools.log_parser import LogParser
        expected_nr_events = 18
        expected_nr_started = 10
        expected_nr_completed = 3
        expected_nr_failed = 5
        file_name = 'data/test.log'
        log_parser = LogParser()
        events = log_parser.parse(file_name)
        self.assertEquals(expected_nr_events, len(events))
        self.assertEquals(expected_nr_started,
                          len(filter(lambda x: x.type == 'started',
                                     events)))
        self.assertEquals(expected_nr_completed,
                          len(filter(lambda x: x.type == 'completed',
                                     events)))
        self.assertEquals(expected_nr_failed,
                          len(filter(lambda x: x.type == 'failed',
                                     events)))
        last_time = datetime.now()
        for event in reversed(events):
            self.assertTrue(last_time >= event.time_stamp)
            last_time = event.time_stamp

    def test_parse_non_existent(self):
        from vsc.atools.log_parser import LogParser
        log_parser = LogParser()
        try:
            events = log_parser.parse('blabla')
            self.assertTrue(False)
        except IOError:
            pass 


if __name__ == '__main__':
    unittest.main()
