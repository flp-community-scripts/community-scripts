"""
Copyright 2024 Olivier Stuker a.k.a. BinaryBorn
"""

import math

from kakibuffer import Buffer
from kakigeometryutils import getFigurePlane
from kakiprimitives import vec4, figure, phenotype
from kakirasterutils import (
  edgeFunction,
  slpipPointInFigureCn,
  slpipPointInFigureWn,
  slpipScanFigure,
)
from kakiutils import getBoundingBox, copyPhenotype, interpolatePhenotypes

"""
Resources:

Rasterizing a triangle
https://jtsorlinis.github.io/rendering-tutorial/

Inclusion of a Point in a Polygon
https://web.archive.org/web/20130126163405/http://geomalgorithms.com/a03-_inclusion.html

"""

def drawFigure(buffer: Buffer, figure: figure, fill: phenotype, fillRule: int = 0):
  """Draws a figure onto buffer.

  Args:
    buffer (Buffer): target buffer
    figure (figure): figure to draw
    fill (phenotype): fill style
    fillRule (int): fill rule (0 = even-odd, otherwise nonzero)
  """

  # switch point in polygon function according to selected rule
  pip = slpipPointInFigureCn if fillRule == 0 else slpipPointInFigureWn

  # cache some properties
  ovs = buffer.oversample
  ox = buffer.originx
  oy = buffer.originy
  w = buffer.width
  h = buffer.height

  plane: vec4 | None
  # if zbuffer is on,
  if buffer.zbuffer:
    # ... find plane equation
    plane = getFigurePlane(figure)

  # check all points buffer
  p = vec4(0,0)
  for y in range(h * ovs):
    p.y = y / ovs + oy
    scanline = slpipScanFigure(figure, p.y)

    for x in range(w * ovs):
      p.x = x / ovs + ox
      if (pip(scanline, p.x)):
        i = y * w * ovs + x
        buffer.data[i] = copyPhenotype(fill)
        if buffer.zbuffer:
          buffer.zbuffer[i] = (plane.w - plane.x * p.x - plane.y * p.y) / plane.z

def drawTriangle(buffer: Buffer, verts: list[vec4], phenos: list[phenotype]):
  """Draws a triangle onto buffer.

  Args:
    buffer (Buffer): target buffer
    verts (list[vec2]): the three vertices of the triangle
    phenos (list[phenotype]): phenotype per vertex
  """
  # minimize and clip rect to render in
  bbox = getBoundingBox(verts)
  x0 = max(0, math.floor(bbox.x0 - buffer.originx))
  y0 = max(0, math.floor(bbox.y0 - buffer.originy))
  x1 = min(buffer.width, math.ceil(bbox.x1 - buffer.originx))
  y1 = min(buffer.height, math.ceil(bbox.y1 - buffer.originy))

  # cache some properties
  ovs = buffer.oversample
  ox = buffer.originx
  oy = buffer.originy
  w = buffer.width
  p0 = verts[0]
  p1 = verts[1]
  p2 = verts[2]
  e123 = edgeFunction(p0, p1, p2)
  pheno0 = phenos[0]
  pheno1 = phenos[1]
  pheno2 = phenos[2]

  # nothing to do if the triangle has no area
  if e123 == 0: return

  # check all points in bounding box
  p = vec4(0,0)
  for y in range(y0 * ovs, y1 * ovs):
    p.y = y / ovs + oy
    for x in range(x0 * ovs, x1 * ovs):
      p.x = x / ovs + ox
      # check if point is inside triangle
      e01 = edgeFunction(p0, p1, p)
      e12 = edgeFunction(p1, p2, p)
      e20 = edgeFunction(p2, p0, p)
      # allow CW and CCW triangles
      if (e01 <= 0 and e12 <= 0 and e20 <= 0
          or e01 >= 0 and e12 >= 0 and e20 >= 0):
        # interpolate phenotypes, wheighted according to distance to vertice
        wgt0 = e12 / e123
        wgt1 = e20 / e123
        wgt2 = e01 / e123
        pheno = interpolatePhenotypes([pheno0, pheno1, pheno2], [wgt0, wgt1, wgt2])
        # put point
        i = y * w * ovs + x
        buffer.data[i] = pheno
        if buffer.zbuffer:
          buffer.zbuffer[i] = p0.z * wgt0 + p1.z * wgt1 + p2.z * wgt2