from kakiprimitives import phenotype
from kakiutils import mixPhenotypes

class Buffer:
  def __init__(self, width: int, height: int, optOversample: int = 0):
    self.width = width
    "width of buffer in pixels"
    self.height = height
    "height of buffer in pixels"
    self.oversample: int = 2 ** optOversample
    "how many pixel sub-divisions (per dimension), power of 2"
    self.data: list[phenotype] = [None] * (width * self.oversample) * (height * self.oversample)
    "pixel data, each pixel is described by one phenotype"
    self.originx = 0.0
    "buffer x offset"
    self.originy = 0.0
    "buffer y offset"

  def setOrigin(self, x: float, y: float):
    """Sets the buffer's offset."""
    self.originx = x
    self.originy = y

  def getPhenotypeAt(self, x: int, y: int) -> phenotype:
    """Returns the phenotype at given pixel location. Will perform interpolation in case of oversampling.
    """
    if x < 0 or x >= self.width or y < 0 or y >= self.height: return None

    i = y * self.width + x
    if self.oversample == 1: return self.data[i]

    # build an intermediate buffer that starts with all data in the oversampling rect and gets downsampled recursively
    data = []
    for sy in range(self.oversample):
      i0 = (y * self.oversample + sy) * self.width * self.oversample + x * self.oversample
      i1 = i0 + self.oversample
      data.extend(self.data[i0:i1])
    # flattened out recursion
    while len(data) > 1:
      ndata = []
      # mix neighbouring phenotypes
      for i in range(0, len(data), 2):
        ndata.append(mixPhenotypes(data[i], data[i+1]))
      data = ndata
    return data[0]