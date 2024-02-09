"""flp
Title: BBC / functions
Author: phil.n
Category: Archive
Version: Unknown
License: Unknown

Description: 
This script helps with selecting articulations for orchestral libraries. It adds
expression keys to all notes in selected regions and removes duplicates. It is
still a work in progress and may have some bugs.

Thread Link: https://forum.image-line.com/viewtopic.php?t=317751
"""
# -*- coding: utf-8 -*-
"""Functions module for Articulation Scripts for FLStudio

Low level functions for Articulation scripts. Has to be imported
and can be used for UI or UI-Less Versions

Classes:

Functions
    configure: has to be imported and called from scripts with UI
    update: main function to add or update expression notes

Todo:
    * 

@author:         Philipp Noertersheuser
@GIT Repository: 
@License
"""
from flpianoroll import *
Utils.log("Imported Functions")

#Array with strings for expressions
___expressions = []


#---------------------------------------------------------------------------------
#Main functions called from scripts

def configure(expressions: list):
    """configures global variables that are used in the script

    Args:
        expressions (list): String list with articulations used by the instrument
    """
    global ___expressions
    Utils.log("Configuring")
    ___expressions = expressions

def update(noteNumber: int, expressioncount: int, useColor:bool = True):
    """updates the expression for selected notes, or all notes if none are selected

    Args:
        noteNumber (int): Number of note for expression, FLStudio start with 0 as C0 for 
        expressioncount (int): Number of expressions for instrument, needed to delete and cleanup expression
        useColor (bool, optional): if notes should be coloured
    """

    #---------------------------------------------------------------------------------
    #splits the selected notes into notes that are played and expressions
    playNotes = []          #index for notes that are played
    noteStarts = []         #starting positions of notes, without duplicates
    noteLengths = []
    expressionNotes = []    #notes that are used for expressions

    for i in range(score.noteCount):                                    #loop over all selected notes
        if score.getNote(i).number <= expressioncount:    #if note key is higher than expression
            expressionNotes.append(i)                                   #add note index to expression list
        else:
            playNotes.append(i)                                         #otherwise to play notes

    #just for debugging
    #Utils.log("Play: " + ','.join(str(x) for x in playNotes))
    #Utils.log("Expression: " + ','.join(str(x) for x in expressionNotes))

    #---------------------------------------------------------------------------------
    #determineNoteStarts stores the start times of all played notes without duplicates
    noteStarts = []
    for i in playNotes:                 
        if(score.getNote(i).time in noteStarts):                        #check if time of current note is already in list
            pass
        else:
            noteStarts.append(score.getNote(i).time)                    #if not add time to the list
            noteLengths.append(score.getNote(i).length)
    
    #just for debugging
    #Utils.log("Notestarts: " + ','.join(str(x) for x in noteStarts))

    #---------------------------------------------------------------------------------
    #compares expression notes to play notes, adds new ones, deletes old ones and changes the settings
    for i in range(len(noteStarts)):                                            #loop over note starts, chords need only one expression
        if(i > len(expressionNotes)-1):                                         #if there are more notestarts than expression notes
            new_note = Note()                                                   #add a new expression note to the score
            new_note.number = noteNumber                                        
            new_note.time = noteStarts[i] -1                                    #expression is one tick before note
            new_note.length = noteLengths[i]

            if useColor:
                new_note.color = noteNumber                                     #change color for better visibility
            score.addNote(new_note)
        else:                                                                   #update expression note to match the current start time
            Utils.log(str(expressionNotes[i]))
            score.getNote(expressionNotes[i]).time = noteStarts[i]-1
            score.getNote(expressionNotes[i]).number = noteNumber
            score.getNote(expressionNotes[i]).length = noteLengths[i]
            if useColor:
                score.getNote(expressionNotes[i]).color = noteNumber

    if(len(expressionNotes) > len(noteStarts)):                                 #if there are more expression notes, delete those no longer needed
        first = len(noteStarts)
        last = len(expressionNotes)
        for i in range(first, last):                                            #loop over notes no longer needed
            #Utils.log("Deleting: " + str(last - i + 1))     
            score.deleteNote(expressionNotes[last - i + 1])                     #delete notes from end to avoid issues with indexing

    if useColor:
        for i in playNotes:                                                         #update color of played notes to match
            score.getNote(i).color = noteNumber



#---------------------------------------------------------------------------------
#FLStudio functions needed for UI
def createDialog():
    """API function called from FLStudio to generate Dialog

    Returns:
        Form: Form that is created and later used for getting and setting values
    """
    global ___expressions
    Utils.log("Create")
    Form = ScriptDialog("Articulation Manager", "Note: Beta.")      
    Form.AddInputCombo("Expression", ___expressions, 0)
    return Form
	
	  
def apply(Form):
    """API function called from FLStudio when preview or OK is used

    Args:
        Form (Form): Form that is shown and where values are selected
    """
    global ___expressions, ___basenote
    Utils.log("Apply")
    update(Form.GetInputValue("Expression"), len(___expressions))