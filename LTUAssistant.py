#!/usr/bin/env python

import argparse
import re
import sys
import settings
import speech
import assistantdb

def CoreNLPFail(sentence):
    words = sentence.split()
    possibleVerb = words[0].lower()
    if possibleVerb in ("show", "plan"):
        return possibleVerb, sentence[len(possibleVerb)+1:]

def Integrate(optional_message = None):
    import CoreNLP
    if optional_message:
        sentence = optional_message
        print "Text input provided: '" + optional_message + "'"
    else:
        greeting_str = 'Hi ' + settings.username.capitalize()
        greeting_str += '! What can I help you with?'
        speech.speak(greeting_str, True)
        (success, sentence) = speech.listen()
        if not success:
            speech.speak(sentence, True)
            exit()
    # CoreNLP is weird, need to replace some stuff to make it properly recognize short sentences
    sentence = sentence.replace("Start", "start").replace("open", "Open").replace("Please", "").replace("please", "")

    # Call NLP parsing function
    (verb, verb_object, noun2, verb2, preposition, adjective) = CoreNLP.Parse(sentence)

    # Fix some more edge cases with broken sentences
    if not verb:
        verb, verb_object = CoreNLPFail(sentence)

    # TODO: Eventually we should probably not attach the preposition to the verb (does it actually improve accuracy?)
    if preposition:
        verb = "%s %s" % (verb, preposition)
        verb_object = noun2

    if not assistantdb.parse(verb.lower(), verb_object.lower(), noun2.lower(), verb2.lower(), adjective.lower()):
        # Text not understood; check for hardcoded special commands we
        # otherwise can't properly handle yet, like settings
        username_regex = re.compile('(hello |hi )*my name is (.+)')
        if username_regex.search(sentence):
            settings.set_username(username_regex.search(sentence).group(2))
            speech.speak('Pleased to meet you, ' + settings.username + '!', True)
        else:
            speech.speak('Sorry, I don\'t understand what you want.', True)

if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text-only-mode',
                        help='make all user interaction happen in the terminal',
                        action='store_true')
    parser.add_argument('-c', '--command-string',
                        help='user\'s initial command text in string form',
                        type=str)
    args = parser.parse_args()
    # Main code
    if args.text_only_mode:
        speech.text_only_mode = True
    if args.command_string:
        Integrate(args.command_string)
    else:
        Integrate()
