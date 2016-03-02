#!/usr/bin/env python

__author__ = 'noisufnoc'

# TODO: Do something awesome
# TODO: Probably going to use geeknote
# TODO: geeknote has no python module
# TODO: Going to have to use evernote sdk
# TODO: Gotta figure out evernote oauth2
# TODO: Need to figure out Todoist API
# TODO: Might want to email some sort of digest, unless other tool is better
# TODO: Forget email digest, log to Splunk via HEC!
# TODO: remove unused imports

# Thank you https://github.com/inkedmn/enhack-sample for helping me to
#   understand how to find my notes

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.type.ttypes as Types
import sys
import os

from evernote.api.client import EvernoteClient
from ConfigParser import SafeConfigParser

CONFIG = 'config.ini'
if os.path.isfile(CONFIG):
    parser = SafeConfigParser()
    parser.read(CONFIG)

    auth_token = parser.get('evernote', 'token')
else:
    print 'You don\'t have any config'
    sys.exit(1)

# Init EvernoteClient object with dev token and host
client = EvernoteClient(token=auth_token, sandbox=True)

# Create UserStore instance
user_store = client.get_user_store()
# Create NoteStore instance
note_store = client.get_note_store()

# Retrieve User object
user = user_store.getUser()
print "Username: %s" % user.username
print "Name: %s" % user.name

raw_input("Type return to continue...")

# Search notes for To-Do / Followup
nFilter = NoteStoreTypes.NoteFilter()
nFilter.words = "To-Do / Followup"
resultSpec = NoteStoreTypes.NotesMetadataResultSpec()
resultSpec.includeTitle = True

searchResults = note_store.findNotesMetadata(nFilter, 0, 10, resultSpec)

if len(searchResults.notes):
    for note in searchResults.notes:
        print note.guid
        print note.title
        my_note = note_store.getNote(note.guid, True, True, False, False)
        print my_note.content
else:
    print "Nothing to see here"

# fin.
