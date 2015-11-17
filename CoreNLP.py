# This file does the CoreNLP parsing
# It takes a sentence, uses the CoreNLP wrapper to parse it, and analyzes the parts
#  - Wrapper is here: https://github.com/brendano/stanford_corenlp_pywrapper
# the things we are interested are the "pos" part (parts of speech),
#  - Documented here: http://www.comp.leeds.ac.uk/amalgam/tagsets/upenn.html
# and the "deps_basic" part, which contains the relationship between words
#  - Documented here: http://nlp.stanford.edu/software/dependencies_manual.pdf
# Using both of these, it can find the most relevant noun and verb to be parsed


from stanford_corenlp_pywrapper import CoreNLP

print("************************* Loading CoreNLP *****************************")
proc = CoreNLP("parse")
print("************************* CoreNLP loaded! *****************************")



def ParseText(text):
	return proc.parse_doc(text)


# Looks for the first word in the sentence with a part of speech starting in "V"
# Returns that verb, and also the word before that if it is an adverb / determiner
def GetVerb(parsed):
	for word in range(len(parsed["tokens"])):
		# found a verb
		if parsed["pos"][word].startswith("V"):
			# found an adverb / determiner
			if word > 0 and parsed["pos"][word-1].startswith("W"):
				return (word-1, word+1) #"%s %s" % (parsed["tokens"][word-1], parsed["tokens"][word])
			else:
				return (word, word+1) #parsed["tokens"][word]
			#(parsed["lemmas"][word], parsed["tokens"][word], parsed["pos"][word])

# Support sentences such as "Tell me where room S202 is"
# Previously would find "Tell" as verb and "me" as subject, and not see anything else at all. The tell me isn't relevant here though
# Searches for a ccomp to hopefully find the real verb
def ConfirmVerb(parsed, verb):
	newverbcheck = FindDependency(parsed, verb, "ccomp")
	if newverbcheck and parsed["pos"][newverbcheck[0]].startswith("V"):
		# this finds the word "where" based on the is
		otherThing = FindDependency(parsed, newverbcheck, "advmod")
		if otherThing:
			return otherThing, newverbcheck
	return verb

# This function searches "deps_basic" to find relationships between words
# It is passed in the position of the word(s) that we relationship is on
# And then searches for any dependencies of the type we want on those words
def FindDependency(parsed, verbPos, depType):
	for dep in parsed["deps_basic"]:
		if dep[0] == depType and dep[1] in range(verbPos[0], verbPos[1]):
			return (dep[2], dep[2]+1)

# Look for the subject of a sentence (based on a verb we already found)
def GetSubject(parsed, verbPos):
	# Look for noun subject / direct object of the verb
	ret = FindDependency(parsed, verbPos, "nsubj")
	if ret:
		return ret
	ret = FindDependency(parsed, verbPos, "dobj")
	if ret:
		return ret

	# That failed, just return the first noun it finds
	# not very good, this may not be necessary since every sentence I have tried always has a nsubj or dobj on the verb
	nounStart = None
	for word in range(len(parsed["tokens"][verbPos[1]:])):
		if nounStart:
			if not parsed["pos"][word].startswith("N"):
				return (nounStart, word)
		elif parsed["pos"][word].startswith("N"):
			nounStart = word
	if nounStart:
		return (nounStart, len(parsed["tokens"])-1)

# Get Extra data, checking for prepositions that modify things
# Parses some more advanced sentences, with multiple verbs and nouns
def GetExtra(parsed, verbPos):
	newVerb = newSubject = None
	# Find the preposition, and the verb that depends on that preposition
	prep = FindDependency(parsed, verbPos, "prep")
	if not prep:
		newVerb = FindDependency(parsed, verbPos, "xcomp")
		if newVerb:
			prep = FindDependency(parsed, newVerb, "prep")
	# Find the subject based on that preposition
	if prep:
		newSubject = FindDependency(parsed, prep, "pobj")
		if not newSubject:
			# not sure if this is possible
			print("Error parsing preposition")
			return
		# Unfinished, look for time stuff here
		time = FindDependency(parsed, newSubject, "num")
		if time and time[0] < newSubject[1]:
			newSubject = (time[0], newSubject[1])

		#newVerb = FindDependency(parsed, prep, "dobj")
	return newSubject, newVerb, prep

# helper function to get / parse a thing we found
def GetWords(parsed, wordPositions):
	if not wordPositions:
		return ""
	return " ".join(parsed["tokens"][wordPositions[0]:wordPositions[1]])

def Parse(text):
	parsed = ParseText(text)["sentences"]
	verb = noun = newNoun = newVerb = prep = otherThing = None
	# Search through all sentences, but we only actually use the first one
	for sentence in parsed:
		print(sentence)
		verb = GetVerb(sentence)
		if verb:
			print(GetWords(sentence, verb))

			# support some fancier sentences
			otherThing, newverbcheck = ConfirmVerb(sentence, verb)
			if otherThing and newverbcheck:
				verb = newverbcheck
				print("Changing verb to %s" % GetWords(sentence, verb))

			noun = GetSubject(sentence, verb)
			if noun:
				print(GetWords(sentence, noun))
			else:
				print("Could not find the subject")

			newNoun, newVerb, prep = GetExtra(sentence, verb)
			if newNoun:
				print("New Noun: " + GetWords(sentence, newNoun))
			if newVerb:
				print("New Verb: " + GetWords(sentence, newVerb))
			if prep:
				print("Prep: " + GetWords(sentence, prep))
		else:
			print("Could not find any verbs")
		# just return the first sentence only for now
		print("\n")

		finalVerb = GetWords(sentence, verb)
		if otherThing:
			finalVerb = "%s %s" % (GetWords(sentence, otherThing), finalVerb)
		return finalVerb, GetWords(sentence, noun), GetWords(sentence, newNoun), GetWords(sentence, newVerb), GetWords(sentence, prep)




# http://www.comp.leeds.ac.uk/amalgam/tagsets/upenn.html  <- parts of speech reference
# http://nlp.stanford.edu/software/dependencies_manual.pdf <- dependencies reference
# https://github.com/brendano/stanford_corenlp_pywrapper
