#!/usr/bin/python3

import csv

class CalendarEvent():
    '''Class for storing calendar event information.'''
    def __init__(self, event_str='', date_str='', start_time_str='', end_time_str=''):
        '''Initialize this CalendarEvent instance.'''
        self.event_str = event_str
        self.date_str = date_str
        self.start_time_str = start_time_str
        self.end_time_str = end_time_str

def read_events():
    '''Returns a list of CalendarEvents from the calendar DB CSV file.'''
    event_list = []
    with open('calendar.csv', 'rb') as calendar_csv:
        calreader = csv.reader(calendar_csv, delimiter=',', quotechar='"')
        for row in calreader:
            print(', '.join(row))
            event_list.append(CalendarEvent(row[0], row[1], row[2], row[3]))
    return event_list

def add_event(ce):
    '''Adds a new event in list form to the calendar DB CSV file.
    Takes a CalendarEvent object.'''
    with open('calendar.csv', 'wb') as calendar_csv:
        calwriter = csv.writer(calendar_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cal_row = [ce.event_str, ce.date_str, ce.start_time_str, ce.end_time_str]
        calwriter.writerow(cal_row)
