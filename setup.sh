#!/bin/bash

if [ ! -d stanford-corenlp-full-2014-08-27 ]; then
	printf "\033[1;34mDownloading CoreNLP jar files (this may take a long time)\033[m\n\n"
	wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip
	unzip stanford-corenlp-full-2014-08-27.zip
	rm stanford-corenlp-full-2014-08-27.zip
fi

if [ ! -d stanford_corenlp_pywrapper ]; then
	printf "\033[1;34mDownloading CoreNLP wrapper library\033[m\n\n"
	git clone https://github.com/brendano/stanford_corenlp_pywrapper.git
	cp libfix.diff stanford_corenlp_pywrapper
	pushd ./stanford_corenlp_pywrapper
	git apply libfix.diff
	popd
fi

printf "\033[1;31mInstalling libraries, this requires root (please enter your password)\033[m\n\n"
printf "\033[1;34mInstalling apt-get libraries\033[m\n\n"
sudo apt-get install python python-notify2 python-pip python-pyaudio espeak flac default-jre
printf "\033[1;34mInstalling Speech Recognition library via pip\033[m\n\n"
sudo pip install SpeechRecognition
printf "\033[1;34mInstalling CoreNLP wrapper\033[m\n\n"
pushd ./stanford_corenlp_pywrapper
sudo pip install .
