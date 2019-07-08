import utils as utils

class Blosum:
  def __init__(self, filename):
    f = open(filename, "r")
    lines = f.read().splitlines()[6::]
    self.matrix = utils.init_matrix(len(lines)-1, len(lines)-1)
    self.indexOf = {}
    for row, line in enumerate(lines):
      if row == 0:
        proteins = line.strip().split()
        for col, protein in enumerate(proteins):
          self.indexOf[protein] = col
      else:
        vals = line.strip().split()[1:]
        for col, val in enumerate(vals):
          self.matrix[row-1][col] = val

  def valueOf(self, p1, p2):
    return self.matrix[self.indexOf[p1]][self.indexOf[p2]]


# b = Blosum("BLOSUM62.txt")
# val = b.valueOf('*','*')
# print(val)