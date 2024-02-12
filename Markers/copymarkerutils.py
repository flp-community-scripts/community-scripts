import flpianoroll as flp

def escape(string: str):
  """Escapes characters (reserved for markers serialization) in string.
  """
  string = string.replace('\\', '\\u005c') # escape char
  string = string.replace(',', '\\u002c') # field delimiter
  string = string.replace(';', '\\u003b') # marker delimiter
  return string

def unescape(string: str):
  """Unescapes characters in string.
  """
  i = 0
  while True:
    # look for escape sequence, exit if none is found
    # start looking AFTER the last replacement, otherwise crafted replacement sequences get replaced twice (\u005cu003b became \u003b and then ;)
    i = string.find('\\u', i + 1)
    if i == -1: break
    # get char code and replace escape sequence
    hex = string[i+2:i+6]
    char = chr(int(hex, 16))
    string = string[:i] + char + string[i+6:]

  return string

def serialize(markers: list, timeOffset: int = 0) -> str:
  """Serializes markers to text.

  Args:
    markers (list): Markers to serialize
    timeOffset (int): Optional, ppq time offset applied for serialization
  """
  texts = []
  for marker in markers:
    fields = []

    # 0.) ppq independent time
    fields.append(str(round((marker.time - timeOffset) / flp.score.PPQ, 9)))
    # 1.) escaped name
    fields.append(escape(marker.name))
    # 2.) mode
    fields.append(str(marker.mode))

    # time signature markers
    if marker.mode == 8:
      # 3.) tsnum
      fields.append(str(marker.tsnum))
      # 4.) tsden
      fields.append(str(marker.tsden))
    # scale markers
    elif marker.mode == 12:
      # 3.) root note
      fields.append(str(marker.scale_root))
      # 4.) helpers, comma removed
      fields.append(str(marker.scale_helper).replace(',', ''))

    # join fields
    text = ','.join(fields)

    texts.append(text)

  # join markers
  serialized = ";\r\n".join(texts)

  return serialized

def deserialize(serialized: str, timeOffset: int = 0) -> list:
  """Deserializes markers from text.

  Args:
    serialized (str): Serialized text of markers
    timeOffset (int): Optional, ppq time offset applied to markers
  """
  markers = []

  # split markers
  texts = serialized.split(';')
  for text in texts:
    # split fields
    fields = text.strip().split(',')

    try:
      marker = flp.Marker()
      # 0.) ppq independent time
      marker.time = int(float(fields[0]) * flp.score.PPQ + timeOffset)
      # 1.) escaped name
      marker.name = unescape(fields[1])
      # 2.) mode
      marker.mode = int(fields[2])
      # time signature markers
      if marker.mode == 8:
        # 3.) tsnum
        marker.tsnum = int(fields[3])
        # 4.) tsden
        marker.tsden = int(fields[4])
      # scale markers
      elif marker.mode == 12:
        # 3.) root note
        marker.scale_root = int(fields[3])
        # 4.) helpers, comma removed
        marker.scale_helper = ','.join(fields[4])

      # if no exception occured, store that marker
      markers.append(marker)
    except Exception:
      pass

  return markers