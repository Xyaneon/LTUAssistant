#!/usr/bin/python3

import argparse
import speech
import subprocess
import sys
import webbrowser
import web

def process_website(site_name, verbose):
    '''Take appropriate action with the given site name.
    The site_name can either be an actual website name or a valid URL.'''
    if site_name in ['bannerweb', 'banner', 'registration', 'financial aid']:
        speech.speak('Opening BannerWeb...', verbose)
        webbrowser.open('https://www.ltu.edu/bannerweb')
    elif site_name in ['blackboard', 'bb']:
        speech.speak('Opening BlackBoard...', verbose)
        webbrowser.open('https://my.ltu.edu')
    elif site_name in ['library', 'ltu library']:
        speech.speak('Opening the LTU Library homepage...', verbose)
        webbrowser.open('https://www.ltu.edu/library')
    elif site_name in ['help desk', 'helpdesk', 'tech support', 'ehelp']:
        speech.speak('Opening LTU eHelp homepage...', verbose)
        webbrowser.open('http://www.ltu.edu/ehelp/')
    elif site_name in ['password', 'mypassword']:
        speech.speak('Opening MyPassword web service...', verbose)
        webbrowser.open('https://mypassword.campus.ltu.edu/')
    elif site_name in ['ltu.edu', 'ltu website', 'ltu homepage']:
        speech.speak('Opening the main LTU website...', verbose)
        webbrowser.open('http://www.ltu.edu')
    elif site_name in ['email', 'webmail', 'mail', 'gmail']:
        speech.speak('Opening Gmail...', verbose)
        webbrowser.open('https://gmail.com')
    elif site_name in ['calendar', 'schedule', 'events']:
        speech.speak('Opening Google Calendar...', verbose)
        webbrowser.open('https://calendar.google.com')
    # Khalil added this
    elif site_name == 'weather':
        degrees, status = web.GetWeatherInfo()
        speech.speak("It is " + degrees + " degrees and " + status.lower() + ".", verbose)
    elif site_name in ['ltu events', 'ltu event']:
        speech.speak('Opening ltu events...', verbose)
        webbrowser.open('http://www.ltu.edu/myltu/calendar.asp')
    else:
        speech.speak('Opening website: ' + site_name, verbose)
        webbrowser.open(site_name)

def process_send_email(recipient_info, verbose):
    '''Take appropriate action with the given email recipient information.'''
    if recipient_info:
        recipient = 'mailto:' + recipient_info  # Open default email client
    else:
        recipient = 'https://mail.google.com/mail/u/0/#compose' # Gmail
    speech.speak('Composing an email...', verbose)
    webbrowser.open(recipient)

def process_find_room(room_str, verbose):
    '''Try to provide information for a given room number.'''
    finder_message = ''
    if room_str:
        # TODO: Use a regular expression for better room number validity
        if len(room_str) >= 2:
            room_letter = room_str.upper()[0]
            room_floor = room_str.upper()[1]
            building_dict = {'A': 'Architecture Building',
                             'B': 'Business Services Building',
                             'C': 'A. Alfred Taubman Student Services Center',
                             'D': 'Art and Design Center',
                             'F': 'CIMR Building',
                             'E': 'Engineering Building',
                             'R': 'Ridler Field House and Applied Research Center',
                             'M': 'Wayne H. Buell Management Building',
                             'S': 'Arts and Sciences Building',
                             'T': 'University Technology and Learning Center'
                            }
            if room_letter in building_dict.keys():
                building = building_dict[room_letter]
            else:
                building = ''

            if building != '':
                finder_message = 'Your room is in the ' + building + ' on floor ' + room_floor + '.'
            else:
                finder_message = 'Sorry, I don\'t know which building that is.'
        else:
            finder_message = 'Sorry, but I don\'t think that\'s a valid room number.'
    else:
        finder_message = 'Sorry, but I don\'t think you told me which room you want.'
    speech.speak(finder_message, verbose)

def parse(verb, verb_object, alternate_verb, alternate_noun, verbose=False):
    browse_cmd_list = ['start', 'open', 'go', 'go to', 'browse', 'browse to', 'launch', 'take to', 'show'] #Original verb only + addition verb 'show'
    email_cmd_list = ['email', 'compose', 'send']
    roomfinder_cmd_list = ['find', 'where is']

    if verb in browse_cmd_list:
        # Open an indicated web page in the default browser
        process_website(verb_object, verbose)
    elif verb in email_cmd_list:
        # Open a window to compose an email
        process_send_email(verb_object, verbose)
    elif verb in roomfinder_cmd_list:
        # Tell the user which building and floor a room is in
        process_find_room(verb_object, verbose)
    else:
        speech.speak('Sorry, I don\'t understand what you want.', verbose)

# For executing this module on its own:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('verb', type=str, help='Assistant database command.')
    parser.add_argument('verb_object', type=str, help='Object passed to command.')
    parser.add_argument('-v', '--verbose',
                        help='Explain what action is being taken.',
                        action='store_true')
    args = parser.parse_args()

    if args.verbose:
        print(sys.version)
    parse(args.verb, args.verb_object, None, None, args.verbose)
    exit()
