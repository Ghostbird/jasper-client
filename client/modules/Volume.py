# -*- coding: utf-8-*-
from __future__ import print_function
from client import app_utils
import re
import os.path
import subprocess
import random

WORDS = ["HIGHER", "LOWER", "INCREASE", "DECREASE", "VOLUME"]

PRIORITY = 3

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with the
        status of the motion daemon, and whether they want to change it.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    if 'volume' not in profile or 'up' not in profile['volume'] or 'down' not in profile['volume']:
        mic.say('The Volume module does not seem to be set-up correctly.')
        mic.say('Please add volume up and volume down configuration options to you profile.')
        return
    volup = profile['volume']['up']
    voldown = profile['volume']['down']
    responses = ['Hey, something is wrong. I am not supposed to say this.']
    if bool(re.search(r'\b(higher|increase)\b', text, re.IGNORECASE)):
        subprocess.call(volup)
        responses = ['Turn it up to eleven!', 'Louder.', 'Yes!']
    elif bool(re.search(r'\b(lower|decrease)\b', text, re.IGNORECASE)):
        subprocess.call(voldown)
        responses = ['Speak softly.', 'Quieter.', 'Yes.', 'Hush.']
    mic.say(random.choice(responses))

def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(higher|lower|increase|decrease) volume\b', text, re.IGNORECASE))
