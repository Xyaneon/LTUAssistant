#!/usr/bin/python3

import csv

def read_events():
    '''Returns a list of scheduled events from the calendar DB CSV file.'''
    event_list = []
    with open('calendar.csv', 'rb') as calendar_csv:
        calreader = csv.reader(calendar_csv, delimiter=',', quotechar='"')
        for row in calreader:
            print(', '.join(row))
            event_list.append(row)
    return event_list

def add_event(event_item_list):
    '''Adds a new event in list form to the calender DB CSV file.'''
    with open('calendar.csv', 'wb') as calendar_csv:
        calwriter = csv.writer(calendar_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        calwriter.writerow(event_item_list)
