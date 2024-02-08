from flpianoroll import *


def print(*x):
  Utils.ShowMessage(str(x))


def clear_notes():
  for i in range(score.noteCount):
    score.deleteNote(0)


def get_notes_list():
  notes = []

  for i in range(score.noteCount):
    note = score.getNote(i)

    notes.append(note)


def clone_pitches(pitches):
  new_pitches = {}

  for pitch, notes in pitches.items():
    new_pitches[pitch] = [note for note in notes]

  return new_pitches


def get_notes_by_pitch():
  pitches = {}

  for i in range(score.noteCount):
    note = score.getNote(i)

    if note.number not in pitches:
      pitches[note.number] = [(note, i)]
    else:
      pitches[note.number].append((note, i))

  return pitches


def sort_pitches_by_time(pitches):
  for p, notes in pitches.items():
    pitches[p] = sorted(notes, key=lambda x: x[0].time)


def sort_pitches_by_end_time(pitches):
  for p, notes in pitches.items():
    pitches[p] = sorted(notes, key=lambda x: x[0].time + x[0].length)


def get_min_time_from_pitches(pitches_by_time):
  pvals = pitches_by_time.values()
  pmin = next(iter(pitches_by_time.values()))[0][0].time

  for pv in pvals:
    first = pv[0][0]
    if (first.time) < pmin:
      pmin = first.time

  return pmin


def get_max_end_time_from_pitches(pitches_by_end_time):
  pvals = pitches_by_end_time.values()
  it = next(iter(pitches_by_end_time.values()))[-1][0]

  t = it.time
  pmax = note_end_time(it)

  for pv in pvals:
    last = pv[-1][0]
    et = note_end_time(last)
    if et > pmax:
      pmax = et
      t = last.time

  return pmax, t


def exclude_overlaps_from_pitches(pitches):
  new_pitches = {}

  for pitch, notes in pitches.items():
    new_notes = []
    excluded = {}

    for i in range(0, len(notes)):
      for j in range(0, len(notes)):
        if notes[j][1] in excluded:
          continue
        if notes[i][0].time < notes[j][0].time and note_end_time(
          notes[i][0]
        ) > note_end_time(notes[j][0]):
          excluded[notes[j][1]] = True
          continue
        new_notes.append(notes[j])

    new_pitches[pitch] = new_notes

  return new_pitches


def note_end_time(note):
  return note.time + note.length
