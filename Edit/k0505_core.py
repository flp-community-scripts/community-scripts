import flpianoroll as flp

class NoteUtils:
    SHARP_TO_FLAT = {
        "c#": "db",
        "d#": "eb",
        "f#": "gb",
        "g#": "ab",
        "a#": "bb"
    }

    @staticmethod
    def translate(
        note: str,
        pitch: bool = False,
        german: bool = False
    ) -> str:
        note_lower = note.lower()
        
        # convert sharp to its flat enharmonic equivalent
        flat_note = NoteUtils.SHARP_TO_FLAT.get(note_lower, note_lower)
        
        # apply German notation rules
        if german:
            german_map = {
                "c": "C",
                "db": "D♭" if pitch else "Db",
                "d": "D",
                "eb": "E♭" if pitch else "Eb",
                "e": "E",
                "f": "F",
                "gb": "G♭" if pitch else "Gb",
                "g": "G",
                "ab": "A♭" if pitch else "Ab",
                "a": "A",
                "bb": "H♭" if pitch else "Hb",
                "b": "H"
            }
            translated = german_map.get(flat_note, flat_note.upper())
        else:
            translated = flat_note.upper()
            
        # fmt flat/sharp symbols
        if pitch:
            translated = translated.replace("b", "♭").replace("#", "♯")
            
        return translated

#-=-=-=-#

class NoteAnalyzer:
    def __init__(self, score: object, sort: bool = True):
        self.notes = self._process_notes(score, sort)

    def _process_notes(self, notes: object, sort: bool = True) -> object:
        """
        Internal helper to parse, filter selection, and sort notes.
        """
        if hasattr(notes, "noteCount"):
            score = notes
            processed_notes = []
            has_selection = False

            for i in range(score.noteCount):
                note = score.getNote(i)

                if note.selected:
                    has_selection = True

                processed_notes.append({
                    "index": i,
                    "note": note
                })

            if has_selection:
                processed_notes = [e for e in processed_notes if e["note"].selected]

            notes_to_sort = processed_notes
        else:
            notes_to_sort = list(notes)

        if sort and notes_to_sort:
            if isinstance(notes_to_sort[0], dict):
                notes_to_sort.sort(key=lambda x: (x["note"].time, x["index"]))
            else:
                notes_to_sort.sort(key=lambda x: x.time)

        return notes_to_sort

    def get_notes(self) -> object:
        """
        Returns the processed and stored notes.
        """
        return self.notes

    def has_chord(self) -> bool:
        """
        Determines if self.notes have any chord-alike sequence.
        
        Returns:
            bool:
                True if any notes in self.notes start at the same time, False otherwise.
        """
        if len(self.notes) < 2:
            return False

        extracted_notes = [
            e["note"] if isinstance(e, dict) else e 
            for e in self.notes
        ]

        for i in range(1, len(extracted_notes)):
            if extracted_notes[i].time == extracted_notes[i - 1].time:
                return True

        return False

    def chord(self, flat: bool = False, pitch: bool = False, german: bool = False) -> str | None:
        """
        Determines chord name in self.notes, supporting flat, pitch symbols, and German notation.
        """
        if not self.notes:
            return None

        extracted_notes = [
            e["note"] if isinstance(e, dict) else e 
            for e in self.notes
        ]

        midi_notes = sorted(list(set(n.Number for n in extracted_notes)))

        if len(midi_notes) < 2:
            return None

        root = midi_notes[0]
        intervals = tuple((n - root) % 12 for n in midi_notes)

        chord_dictionary = {
            # Triads
            (0, 4, 7): "Major",
            (0, 3, 7): "Minor",
            (0, 3, 6): "Diminished",
            (0, 4, 8): "Augmented",
            (0, 5, 7): "Suspended 4th",
            (0, 2, 7): "Suspended 2nd",

            # Sevenths
            (0, 4, 7, 10): "Dominant 7th",
            (0, 4, 7, 11): "Major 7th",
            (0, 3, 7, 10): "Minor 7th",
            (0, 3, 6, 9): "Diminished 7th",
            (0, 3, 6, 10): "Half-Diminished 7th",
            (0, 4, 8, 10): "Augmented 7th",
            (0, 5, 7, 10): "7sus4",

            # Sixths
            (0, 4, 7, 9): "Major 6th",
            (0, 3, 7, 9): "Minor 6th",

            # Ninths & Adds
            (0, 2, 4, 7): "Add 9",
            (0, 2, 3, 7): "Minor Add 9",
            (0, 2, 4, 7, 11): "Major 9th",
            (0, 2, 3, 7, 10): "Minor 9th"
        }

        sharp_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        flat_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

        raw_note = flat_names[root % 12] if flat else sharp_names[root % 12]
        root_name = NoteUtils.translate(raw_note, pitch = pitch, german = german)

        chord_type = chord_dictionary.get(intervals)

        if chord_type:
            return f"{root_name} {chord_type}"

        return None

    def determine_duration(self) -> int:
        """
        Calculates the total duration from the first note start to the last note end.
        """
        if not self.notes:
            return 0
            
        first_note = self.notes[0]["note"]
        phrase_start = first_note.time
        phrase_end = max(e["note"].time + e["note"].length for e in self.notes)

        return phrase_end - phrase_start

def log(*args, sep = " ", end = "\n"):
	args = list(args)

	if "__title__" in globals():
		args = [f"{__title__}: ", *args]

	retval = sep.join(args) + end
	retval = retval.strip()

	flp.Utils.log(retval.replace("\n", "; "))
	flp.Utils.ShowMessage(retval)

	return