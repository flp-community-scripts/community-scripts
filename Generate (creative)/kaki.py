"""
Kaki engine (rasterizer for FL Studio).

Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

# A word on coordinates:
# +X is to the right (same direction as time in PR)
# +Y is up (same direction as MIDI note number in PR)
# +Z is out of screen (established by the right hand rule)
# Incidentally, this is the same as in OpenGL

# everything happens in 3d space

# 3d coordinates are homogeneous, meaning they all have a fourth component called w (x, y, z, w).

# therefore, all the matrices are 4x4 as well

# perspective projection has to be applied explicitly before rendering

from kakibuffer import Buffer

from kakigeometryutils import (
  getFigureBoundingBox,
  getMeshBoundingBox,
  getPointsPlane,
  getFigurePlane,
  transformPoints,
  transformFigure,
  transformMesh,
  clonePoints,
  cloneFigure,
  applyPerspectivePoints,
  applyPerspectiveFigure,
  applyPerspectiveMesh,
)

from kakilighting import (
  lightMesh
)

from kakiparsers import (
  parsePhenotypeFromStyle,
  parseFigureFromSvgPath
)

from kakiprimitives import (
  vec4,
  mat4,
  box,
  figure,
  phenotype,
  tri,
  mesh,
)

from kakirasterizer import (
  drawFigure,
  drawTriangle,
  drawMesh,
)

from kakirenderer import render

from kakiutils import (
  getBoundingBox,
  limitBox,
  copyPhenotype,
  mixPhenotypes,
  interpolatePhenotypes,
  getPhenotypeFromNote,
  normvec,
  dotprod,
  crossprod,
  anglevec,
  matmul4,
  transform,
  identity4,
  translate,
  scale,
  rotate,
  rotateX,
  rotateY,
  rotateZ,
  homogeneousPinch,
)

