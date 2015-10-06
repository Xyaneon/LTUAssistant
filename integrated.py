#!/usr/bin/env python

import sys
import speech
import test
import assistantdb

if len(sys.argv) > 1:
	sentence = " ".join(sys.argv[1:])
else:
	(success, sentence) = speech.Listen()
	if not success:
		print(sentence)
		exit()
(verb, verb_object, _, _, _) = test.Parse(sentence)
print(verb, verb_object, "test")
assistantdb.parse(verb.lower(), verb_object.lower())
