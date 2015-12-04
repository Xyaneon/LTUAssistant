#!/usr/bin/python3

import configparser, os

# Initialize INI file path
folder = os.path.join(os.path.expanduser('~'), '.LTUAssistant')
try:
    os.makedirs(folder)
except OSError:
    if not os.path.isdir(folder):
        raise
settings_ini_path = os.path.join(folder, 'settings.ini')

# Default settings
username = 'student'
voice = 'male'

config = configparser.ConfigParser()
if not os.path.isfile(settings_ini_path):
    # Set up default settings
    config['Basic'] = {'username': username,
                       'voice': voice}
    with open(settings_ini_path, 'w') as configfile:
        config.write(configfile)
else:
    # Read in pre-recorded settings
    config.read(settings_ini_path)
    username = config['Basic']['username']
    voice = config['Basic']['voice']

def set_username(name_str=''):
    '''Sets the username if provided.'''
    global username
    if not name_str.lower() == '':
        config['Basic']['username'] = name_str
        username = name_str
    with open(settings_ini_path, 'w') as configfile:
        config.write(configfile)

def set_voice(voice_str='male'):
    '''Sets the desired voice (female if specified, male otherwise).'''
    global voice
    if voice_str.lower() == 'female':
        config['Basic']['voice'] = 'female'
        voice = 'female'
    else:
        config['Basic']['voice'] = 'male'
        voice = 'male'
    with open(settings_ini_path, 'w') as configfile:
        config.write(configfile)
