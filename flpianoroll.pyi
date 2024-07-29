"""Stub file for type checking scripts in VSCode or comparable.
File should be aside of the pyscript file, to be used correctly
"""

from typing import Union


Utils : __utils__
"Use the global Utils to access logging and message boxes"
score : __score__
"Use the global score to access functions for the piano roll score"

#-------------------------------------------------------------------#
#---Utils Class, used for the global Utils
class __utils__():
    """class with utility logging functions
    """
    def log(self, msg: str) -> None:
        """Writes a string to the FL Studio debug log tab. Options=>Debugging Log

        Args:
            msg (str): text to be logged
        """
        pass

    def ShowMessage(self, msg: str) -> None:
        """shows message box with defined string

        Args:
            msg (str): text to be shown
        """
        pass

    def ProgressMsg(self, msg: str, pos: int, total: int) -> None:
        """Shows a progress message

        Args:
            msg (str): text to be shown
            pos (int): current step
            total (int): number of steps
        """
        pass

#-------------------------------------------------------------------#
#---Score Class, used for the global score Variable
class __score__():
    """Score is used to access markers and notes
    """
    noteCount: int
    "nr of notes, read only"
    PPQ : int
    "ticks per quarter note, read only"
    tsnum : int
    "current project time signature numerator, read only"
    tsden : int
    "current project time signature denominator, read only"
    markerCount : int
    "nr of markers, read only"
    snap_root_note: int
    "scale root note (C = 0)"
    snap_scale_helper: str
    """String in the form of `0,1,0,1,0,0,1,0,1,0,1,0`
    with 0 indicating notes *in* the scale and 1 indicating notes
    *not* in scale. This helper is always C-aligned.
    """

    def clear(self, all:bool = False) -> None:
        """remove notes and markers.

        Args:
            all (bool, optional): "True" to clear all, instead of just selected. Defaults to False.
        """
        pass

    def clearNotes(self, all:bool = False) -> None:
        """remove notes.

        Args:
            all (bool, optional): "True" to clear all, instead of just selected. Defaults to False.
        """
        pass

    def clearMarkers(self, all:bool = False) -> None:
        """remove markers.

        Args:
            all (bool, optional): "True" to clear all, instead of just selected. Defaults to False.
        """
        pass

    def addNote(self, note: Note) -> None:
        """add new note to score

        Args:
            note (Note): Note to be added to score
        """
        pass

    def getNote(self, index: int) -> Note:
        """get note by index

        Args:
            index (int): index of note in score

        Returns:
            Note: selected note
        """
        pass

    def deleteNote(self, index: int) -> None:
        """deletes note by index, IMPORTANT: index of notes will change with deletion

        Args:
            index (int): index of note to be deleted
        """
        pass

    def addMarker(self, marker: Marker) -> None:
        """add new marker to score

        Args:
            marker (Marker): Marker to be added to score
        """
        pass

    def getMarker(self, index: int) -> Marker:
        """get marker by index

        Args:
            index (int): index of marker in score

        Returns:
            Marker: selected Marker
        """
        pass

    def deleteMarker(self, index: int) -> None:
        """deletes marker by index, IMPORTANT: index of markers will change with deletion

        Args:
            index (int): index of marker to be deleted
        """
        pass

    def getTimelineSelection(self) -> tuple[int, int]:
        """gets the selected timeline range

        Returns:
            tuple[int, int]: selection start time, selection end time in ticks (end is -1 if no selection was made or if it's been collapsed)
        """
        pass

    def getDefaultNoteProperties(self) -> Note:
        """returns a note with the currently active style

        Returns:
            Note: note with the draw tool's current properties
        """
        pass

    def getNextFreeGroupIndex(self) -> int:
        """Returns the next free note group index. If your script adds multiple groups, make sure to add the notes of one group using addNote before calling this function again to get the updated next free group index.

        Returns:
            Note: Next free not group index
        """
        pass

#-------------------------------------------------------------------#
#---Script Dialog Class
class ScriptDialog():
    """Dialog that is shown when script is called
    """
    def __init__(self, title: str, description: str) -> None:
        """Initializes a new script dialog

        Args:
            title (str): Title of Window
            description (str): Description shown on windo
        """
        pass
        

    def AddInput(self, name: str, value: float) -> None:
        """Adds a generic input control, rotary boolean

        Args:
            name (str): Name of control
            value (float): Initial value
        """
        pass

    def AddInputKnob(self, name: str, value: float, min: float, max: float) -> None:
        """Adds a knob input control with float values

        Args:
            name (str): Name of control
            value (float): Initial value
        """
        pass

    def AddInputKnobInt(self, name: str, value: int, min: int, max: int) -> None:
        """Adds a knob input control with int values

        Args:
            name (str): Name of control
            value (int): Initial value
        """
        pass

    def AddInputCombo(self, name: str, options: list, value: int) -> None:
        """Adds a combo box input control with list of strings

        Args:
            name (str): Name of control
            options (list): Options for selection
            value (int): Index of initial option
        """
        pass

    def AddInputText(self, name: str, value: str) -> None:
        """Adds a text box input control with string value

        Args:
            name (str): Name of control
            value (str): text to display
        """
        pass

    def AddInputCheckbox(self, name: str, value: bool) -> None:
        """Adds a checkbox input control with string value

        Args:
            name (str): Name of control
            value (bool): Initial value
        """
        pass

    def AddInputSurface(self, name: str) -> None:
        """Adds a control surface

        Args:
            name (str): Name of the control surface's preset file (without the `.fst` extension)
        """
        pass

    def GetInputValue(self, name: str) -> Union[str, int, float]:
        """Retrieve the current value of the input with the specified name

        Args:
            name (str): name of control

        Returns:
            Union[str, int, float]: current value of control
        """
        pass

    def Execute(self) -> bool:
        """How the dialog was closed, Returns TRUE if the user pressed OK, FALSE if the dialog was cancelled

        Returns:
            bool: state of dialog
        """

#-------------------------------------------------------------------#
#---Note Class
class Note():
    """Class that contains information about notes from the score
    """

    number: int
    "note number (MIDI standard)"
    time: int
    "in ticks"
    length: int
    "in ticks"
    group: int
    "group number this note belongs to"
    pan: float
    "0.0 to 1.0, default 0.5"
    velocity: float
    "0.0 to 1.0, default 0.8"
    release: float
    "0.0 to 1.0"
    color: int
    "0 to 15, default 0. Color group / MIDI channel."
    fcut: float
    "0.0 to 1.0, default 0.5"
    fres: float
    "0.0 to 1.0, default 0.5"
    pitchofs: int
    "-120 to 120"
    repeats: int
    """0 to 14, default 0
    
    1: 1/4 (beat)
    2: 1/8 dotted
    3: 1/4 triplet
    4: 1/8
    5: 1/16 dotted
    6: 1/8 triplet
    7: 1/16 (step)
    8: 1/32 dotted
    9: 1/16 triplet
    10: 1/32 (half step)
    11: 1/64 dotted
    12: 1/32 triplet
    13: 1/64 (quarter step)
    14: 1/64 triplet
    """
    slide: bool
    "slide is enabled"
    porta: bool
    "portamento enable"
    muted: bool
    "note is muted"
    selected: bool
    "note is selected"

    def clone(self) -> Note:
        """current note is cloned
        """

#-------------------------------------------------------------------#
#---Marker Class
class Marker():
    """class for information about marker
    """
    time: int
    "in ticks"
    name: str
    "marker name"
    mode: int
    "mode of marker as integer"
    tsnum: int
    "when marker is a time signature"
    tsden: int
    "when marker is a time signature"
    scale_root: int
    "scale root note (C = 0)"
    scale_helper: str
    """String in the form of `0,1,0,1,0,0,1,0,1,0,1,0`
    with 0 indicating notes *in* the scale and 1 indicating notes
    *not* in scale. This helper is always C-aligned.
    """