"""flp
Title: BBC / articulations
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

class ___bbcso:
    Instruments = [ "Violins", "Violas", "Celli", "Basses", "Horns", "HornsA4", "Trumpet", "TrumpetsA3", "TenorTrombone", "TenorTrombonesA3", "BassTrombonesA2", "Tuba", "Flutes", "FlutesA3", "Piccolo", "Oboe", "OboesA3", "Clarinet", "ClarinetsA3", "Bassoon", "BassoonsA3", "UntunedPercussion", "Timpani", "Harp", "Marimba", "Celeste", "Xylophone",  "Glockenspiel",  "TubularBells", "Vibraphone",  "Crotales"]
    Violins = [ "Legato", "Long", "Long CS", "Long Flautando", "Spiccato", "Staccato", "Pizzicato", "Col Legno", "Tremolo", "Trill Major 2nd", "Trill Minor 2nd", "Long Sul Tasto", "Long Harmonics", "Short Harmonics", "Bartok Pizzicato", "Long Marcato Attack", "Tremolo Sul Pont", "Tremolo CS", "Long Sul Pont", "Spiccato CS" ]
    Violas = [ "Legato", "Long", "Long CS", "Long Flautando", "Spiccato", "Staccato", "Pizzicato", "Col Legno", "Tremolo", "Trill Major 2nd", "Trill Minor 2nd", "Long Sul Tasto", "Long Harmonics", "Short Harmonics", "Bartok Pizzicato", "Long Marcato Attack", "Tremolo Sul Pont", "Tremolo CS", "Long Sul Pont", "Spiccato CS" ]
    Celli = [ "Legato", "Long", "Long CS", "Long Flautando", "Spiccato", "Staccato", "Pizzicato", "Col Legno", "Tremolo", "Trill Major 2nd", "Trill Minor 2nd", "Long Sul Tasto", "Long Harmonics", "Short Harmonics", "Bartok Pizzicato", "Long Marcato Attack", "Tremolo Sul Pont", "Tremolo CS", "Long Sul Pont", "Spiccato CS" ]
    Basses = [ "Legato", "Long", "Long CS", "Long Flautando", "Spiccato", "Staccato", "Pizzicato", "Col Legno", "Tremolo", "Trill Major 2nd", "Trill Minor 2nd", "Long Sul Tasto", "Long Harmonics", "Short Harmonics", "Bartok Pizzicato", "Long Marcato Attack", "Tremolo Sul Pont", "Tremolo CS", "Long Sul Pont", "Spiccato CS" ]
    Horn = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue", "Trill Major 2nd", "Trill Minor 2nd"]
    HornsA4 = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue", "Trill Major 2nd", "Trill Minor 2nd"]
    Trumpet = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue", "Trill Major 2nd", "Trill Minor 2nd"]
    TrumpetsA3 = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue", "Trill Major 2nd", "Trill Minor 2nd"]
    TenorTrombone = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue"]
    TenorTrombonesA3 = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue"]
    BassTrombonesA2 = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue"]
    Tuba = ["Legato", "Long", "Staccatissimo", "Marcato", "Long Cuivre", "Long Sfz", "Long Flutter", "Multi-tongue"]
    Flutes = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Long Flutter", "Multi-tongue" ]
    FlutesA3 = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Long Flutter", "Multi-tongue" ]
    Piccolo = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Long Flutter", "Multi-tongue", "Rips", "Falls" ]
    Oboe = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Multi-tongue" ]
    OboesA3 = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Multi-tongue" ]
    Clarinet = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Multi-tongue" ]
    ClarinetsA3 = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Multi-tongue" ]
    Bassoon = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Long Flutter" ]
    BassoonsA3 = [ "Legato", "Long", "Trill Major 2nd", "Trill Minor 2nd", "Staccatissimo", "Tenuto", "Marcato", "Long Flutter" ]
    UntunedPercussion = ["UntunedAnvil","BassDrum1", "BassDrum2", "Cymbal", "MilitaryDrums", "Piatti", "Snare1", "Snare2", "TamTam", "Tambourine", "TenorDrum", "Toys", "Triangle"]
    Timpani = ["Hits", "Rolls", "Hits Soft", "Rolls Soft", "Hits Hotrods", "Long Rolls Hotrods", "Hits Damped", "Hits Super Damped", "Hotrods Hits Damped", "Hits Damped Soft"]
    Harp = [ "Sustained", "Damped", "Damped Medium", "Bisbigliando Trem", "Gliss FX"]
    Marimba = ["Hits"]
    Celeste = [ "Sustained", "Damped", "Damped Medium"]
    Xylophone = ["Hits", "Rolls"]
    Glockenspiel = ["Hits", "Rolls"]
    TubularBells = ["Hits", "Rolls", "Hits Damped"]
    Vibraphone = ["Hits"]
    Crotales = ["Hits", "Hits Bowed"]	

BBCSO = ___bbcso()