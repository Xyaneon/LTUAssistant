#!/usr/bin/python3

import argparse
import calendardb
import notify2
import speech  # Used here for interactive questions
import settings
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
        process_weather(verbose)
    elif site_name in ['ltu events', 'ltu event']:
        speech.speak('Opening ltu events...', verbose)
        webbrowser.open('http://www.ltu.edu/myltu/calendar.asp')
    else:
        speech.speak("I couldn't understand what website you want to open")

def process_send_email(recipient_info, verbose):
    '''Take appropriate action with the given email recipient information.'''
    if recipient_info and recipient_info.find("@") != -1:
        recipient = 'mailto:' + recipient_info  # Open default email client
    else:
        recipient = 'https://mail.google.com/mail/u/0/#compose' # Gmail
    speech.speak('Composing an email...', verbose)
    webbrowser.open(recipient)

def process_find_room(room_str, verbose):
    '''Try to provide information for a given room number.'''
    finder_message = ''
    if room_str:
        words = room_str.split()
        if words[0] == "room":
            words.remove("room")
        if not len(words) or len(words[0]) not in range(4, 6):
            finder_message = 'Sorry, but I don\'t think you told me which room you want.'
        # TODO: Use a regular expression for better room number validity
        else:
            print(words)
            room_letter = words[0][0].upper()
            room_floor = words[0][1]
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
        finder_message = 'Sorry, but I don\'t think you told me which room you want.'
    speech.speak(finder_message, verbose)

def process_add_cal_event(event_str, verbose):
    '''Schedule a new calendar event with the user.'''
    if event_str == 'event':
        event_sentence = speech.ask_question('Okay, what is the event called?', verbose)
        day_sentence = speech.ask_question('What day will this be on?', verbose)
        time_sentence = speech.ask_question('What time will this start at?', verbose)
        cal_event = calendardb.CalendarEvent(event_sentence, day_sentence, time_sentence, '')
        calendardb.add_event(cal_event)
        feedback_sentence = 'Alright, I\'m putting down ' + str(cal_event) + '.'
        speech.speak(feedback_sentence, verbose)
    else:
        speech.speak('Sorry, I am unable to help you schedule this right now.', verbose)

def process_weather(verbose):
    '''Tells the user what the current weather conditions are.'''
    degrees, status = web.GetWeatherInfo()
    speech.speak("It is " + degrees + " degrees and " + status.lower() + ".", verbose)

def process_schedule(verbose):
    '''Tells the user what events are planned for today from the calendar DB.'''
    event_list = calendardb.get_todays_events()
    if len(event_list) < 1:
        output_str = 'There are no events currently scheduled.'
    elif len(event_list) == 1:
        output_str = ' '.join(['You only have', event_list[0].event_str, 'at',
                               event_list[0].start_time_str]) + '.'
    elif len(event_list) == 2:
        output_str = ' '.join(['You have', event_list[0].event_str, 'at',
                               event_list[0].start_time_str, 'and',
                               event_list[1].event_str, 'at',
                               event_list[1].start_time_str]) + '.'
    else:
        # 3 or more events
        output_str = 'You have '
        for event in event_list[:-1]:
            output_str += ' '.join([event.event_str, 'at',
                                    event.start_time_str]) + ', '
        output_str += ' '.join(['and', event_list[-1].event_str, 'at',
                                event_list[-1].start_time_str]) + '.'
    speech.speak(output_str, verbose)

def process_voice(voice):
    if voice in ("female", "male"):
        settings.set_voice(voice)
        speech.speak('Okay, I will use a %s voice from now on.' % (voice), True)
    else:
        speech.speak('I don\'t understand what voice you want')

def process_name_change(new_name):
    if new_name:
        settings.set_username(new_name)
        speech.speak('Pleased to meet you, ' + settings.username + '!', True)
        return True
    else:
        return False

def parse(verb, verb_object, alternate_noun, alternate_verb, adjective, verbose=False):
    '''Parse the command and take an action. Returns True if the command is
    understood, and False otherwise.'''
    # Print parameters for debugging purposes
    print('\tverb:           ' + verb)
    print('\tverb_object:    ' + verb_object)
    print('\talternate_verb: ' + alternate_verb)
    print('\talternate_noun: ' + alternate_noun)
    print('\tadjective:      ' + adjective)
    browse_cmd_list = ['start', 'open', 'go', 'go to', 'browse', 'browse to', 'launch', 'take to', 'show'] #Original verb only + addition verb 'show'
    email_cmd_list = ['email', 'compose', 'compose to', 'send', 'send to', "write", "write to"]
    roomfinder_cmd_list = ['find', 'where is']
    calendar_cmd_list = ['schedule', 'remind', 'remind about', 'plan']
    voice_cmd_list = ['use']

    if verb in browse_cmd_list:
        # Open an indicated web page in the default browser
        process_website(verb_object, verbose)
    elif verb in email_cmd_list:
        # Open a window to compose an email
        process_send_email(verb_object, verbose)
    elif verb in roomfinder_cmd_list:
        # Tell the user which building and floor a room is in
        process_find_room(verb_object, verbose)
    elif verb in calendar_cmd_list:
        # Schedule an event for the user
        process_add_cal_event(verb_object, verbose)
    elif verb in voice_cmd_list:
        # Change voice between male / female
        process_voice(adjective)
    # This could be a few things
    elif verb == "what is" or verb == "tell":
        if verb_object.find("weather") != -1:
            process_weather(verbose)
        elif verb_object == "schedule":
            process_schedule(verbose)
        elif verb_object == "time":
            speech.speak('It is currently ' + calendardb.get_current_time() + '.', True)
        elif verb_object == "date" or verb_object == "day":
            speech.speak('Today is ' + calendardb.get_current_date() + '.', True)
        else:
            return False
    elif verb == "is":
        if verb_object == "time":
            speech.speak('It is currently ' + calendardb.get_current_time() + '.', True)
        elif verb_object == "date" or verb_object == "day":
            speech.speak('Today is ' + calendardb.get_current_date() + '.', True)
        elif verb_object == "name":
            return process_name_change(alternate_noun)
    elif verb == "call":
        return process_name_change(verb_object or alternate_noun)
    else:
        return False
    return True

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
