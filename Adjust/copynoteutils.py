import flpianoroll as flp

def serialize(notes: list[flp.Note], timeOffset: int = 0) -> str:
  """Serializes notes to text.

  Args:
    notes (list[Note]): Notes to serialize
    timeOffset (int): Optional, ppq time offset applied for serialization
  """
  texts = []
  for note in notes:
    fields = []

    # stringify all properties in a css-like manner (key: value;)
    
    fields.append(f'number: {note.number}')
    fields.append(f'time: {((note.time - timeOffset) / flp.score.PPQ):.9f}')
    fields.append(f'length: {(note.length / flp.score.PPQ):.9f}')
    fields.append(f'pan: {note.pan:.2f}')
    fields.append(f'velocity: {note.velocity:.2f}')
    fields.append(f'release: {note.release:.2f}')
    fields.append(f'color: {note.color}')
    fields.append(f'fcut: {note.fcut:.3f}')
    fields.append(f'fres: {note.fres:.3f}')
    fields.append(f'pitchofs: {note.pitchofs}')
    fields.append(f'repeats: {note.repeats}')
    fields.append(f'slide: {note.slide}')
    fields.append(f'porta: {note.porta}')
    
    texts.append('; '.join(fields))

  return '\n'.join(texts)

def deserialize(serialized: str, timeOffset: int = 0) -> list[flp.Note]:
  """Deserializes notes from text.

  Args:
    serialized (str): Serialized text of notes
    timeOffset (int): Optional, ppq time offset applied to markers
  """
  notes = []

  # split notes
  texts = serialized.split('\n')
  for text in texts:
    # split fields
    fields = text.strip().split(';')

    try:
      note = flp.Note()
      for field in fields:
        pair = field.split(':')
        key = pair[0].strip()
        val = pair[1].strip()
        if key == 'number':
          note.number = int(val)
        elif key == 'time':
          note.time = round(float(val) * flp.score.PPQ + timeOffset)
        elif key == 'length':
          note.length = round(float(val) * flp.score.PPQ)
        elif key == 'pan':
          note.pan = float(val)
        elif key == 'velocity':
          note.velocity = float(val)
        elif key == 'release':
          note.release = float(val)
        elif key == 'color':
          note.color = int(val)
        elif key == 'fcut':
          note.fcut = float(val)
        elif key == 'fres':
          note.fres = float(val)
        elif key == 'pitchofs':
          note.pitchofs = int(val)
        elif key == 'repeats':
          note.repeats = int(val)
        elif key == 'slide':
          note.slide = True if val == 'True' else False
        elif key == 'porta':
          note.porta = True if val == 'True' else False
      
      notes.append(note)
    except Exception:
      pass

  return notes