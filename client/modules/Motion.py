# -*- coding: utf-8-*-
from __future__ import print_function
from client import app_utils
import re
import os.path
import subprocess
import random

WORDS = ["START", "STOP", "WATCHING", "LOOKING", "GUARDING"]

PRIORITY = 3

MOTION_BINARY = '/usr/bin/motion'

class MotionException(Exception):
    pass

def stopMotion(runfile_path):
    with open(runfile_path, 'r') as runfile:
        p = subprocess.Popen(['kill', runfile.read().strip()])
        output, errors = p.communicate()
        if errors:
            raise MotionException(errors)

def startMotion(binary_path):
    subprocess.Popen([binary_path])

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with a with the
        status of the motion daemon, and whether they want to change it.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    if 'motion' not in profile or 'binary' not in profile['motion'] or 'runfile' not in profile['motion']:
        mic.say('Motion does not seem to be set-up correctly.')
        mic.say('Please add motion binary and motion runfile configuration options to you profile.')
        return
    runfile = profile['motion']['runfile']
    binary = profile['motion']['binary']
    responses = ['Hey, something is wrong. I am not supposed to say this.']
    if bool(re.search(r'\bstop\b', text, re.IGNORECASE)):
        if os.path.isfile(runfile):
            stopMotion(runfile)
            responses = ['Have it your way.', 'Enjoy your privacy.', 'I will just close my eyes for a second.', 'You are not that interesting anyway.']
        else:
            responses = ['I was not looking at you.', 'You are delusional, nobody is watching.', 'It was not me. It was the N S A.']
    elif bool(re.search(r'\bstart\b', text, re.IGNORECASE)):
        if os.path.isfile(runfile):
            responses = ['Did you think I was not paying attention?', 'I am already watching.', 'I have been on guard duty for a while already.']
        else:
            startMotion(binary)
            responses = ['I will keep an eye on things.', 'I will guard this room.', 'I will keep careful watch.', 'I will keep my eyes wide open.']
    mic.say(random.choice(responses))

def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(start|stop) (look|watch|guard)ing\b', text, re.IGNORECASE))
