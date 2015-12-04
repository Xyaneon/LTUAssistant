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
