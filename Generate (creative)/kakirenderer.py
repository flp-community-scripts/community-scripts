import flpianoroll

from kakibuffer import Buffer

def render(buffer: Buffer, xoff: int, yoff: int, pixelWidth: int = flpianoroll.score.PPQ / 4):
  """Renders a buffer into flpianoroll.Notes
  """
  notes = []

  for iy in range(buffer.height):
    y = yoff + iy
    if y >= 0 and y < 131:
      for ix in range(buffer.width):
        x = xoff + ix
        if x >= 0:
          pheno = buffer.getPhenotypeAt(ix, iy)
          if pheno is not None:
            note = flpianoroll.Note()
            # position note
            note.time = x * pixelWidth
            note.number = y
            note.length = pixelWidth
            # apply attributes
            note.velocity = pheno.vel
            note.pan = pheno.pan
            note.release = pheno.rel
            note.pitchofs = pheno.pof
            note.fcut = pheno.cut
            note.fres = pheno.res
            note.color = pheno.col
            notes.append(note)

  return notes