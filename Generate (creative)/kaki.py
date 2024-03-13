# A word on coordinates:
# +X is to the right (same direction as time in PR)
# +Y is up (same direction as MIDI note number in PR)
# +Z is out of screen (established by the right hand rule)
# Incidentally, this is the same as in OpenGL

from kakibuffer import Buffer

from kakigeometryutils import (
  getFigureBoundingBox,
  transformPoints,
  transformFigure,
  clonePoints,
  cloneFigure,
  transformPoints3d,
  transformFigure3d,
  clonePoints3d,
  cloneFigure3d,
  extrudePoints,
  extrudeFigure,
  projectPoints,
  projectFigure,
)

from kakiparsers import (
  parsePhenotypeFromStyle,
  parseFigureFromSvgPath
)

from kakiprimitives import (
  vec2,
  vec3,
  mat3,
  mat4,
  box,
  figure,
  figure3d,
  phenotype
)

from kakirasterizer import (
  drawFigure,
  drawTriangle
)

from kakirenderer import render

from kakiutils import (
  getBoundingBox,
  limitBox,
  interpolatePhenotypes,
  matmul3,
  matmul4,
  mixPhenotypes,
  transform
)

