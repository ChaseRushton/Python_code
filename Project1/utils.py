# Parses a fasta file and returns an array of its sequence
def fasta_to_seq(filename):
  f = open(filename, "r")
  l = [str.strip() for str in f.readlines()[1:]]
  seq = list("".join(l))
  f.close()
  return seq

def init_matrix(w, h):
  return [[0 for col in range(w)] for row in range(h)]




# def print_2d(m):
#   for x in m:
#     print(x)