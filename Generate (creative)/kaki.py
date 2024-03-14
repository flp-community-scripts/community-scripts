# A word on coordinates:
# +X is to the right (same direction as time in PR)
# +Y is up (same direction as MIDI note number in PR)
# +Z is out of screen (established by the right hand rule)
# Incidentally, this is the same as in OpenGL

# 2d coordinates are cartesian, meaning they only have two components (x, y).
# 2d transformation matrices are 3x3 so they can be combined.
# Applying a 2d transformation matrix will assume the vector's missing component to be 1 and ignore the 3 row in the matrix completely.

# 3d coordinates are homogeneous, meaning they all have a fourth component called w (x, y, z, w).

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
  augmentPoints,
  augmentFigure,
  projectPoints,
  projectFigure,
)

from kakiparsers import (
  parsePhenotypeFromStyle,
  parseFigureFromSvgPath
)

from kakiprimitives import (
  vec2,
  vec4,
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
  transform,
  transform3d,
  identity3,
  identity4,
  translate,
  scale,
  rotate,
  translate3d,
  scale3d,
  rotateX3d,
  rotateY3d,
  rotateZ3d,
  perspective3d,
)

