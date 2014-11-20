#-----------------------------------------------------------------------------#
# Name: dynamicprogramming.py
# Desc: Implementation for Dynamic Programming Project in CS 325
# Auth: Cezary Wojcik, Sean McGlothlin, Matthew Eilertson
# Note:
# Opts: -i, --inputfile     : specify input file (defaults to "test.txt")
#       -o, --outputfile    : specify output file for results
#       -d, --debug           : show debug messages
#-----------------------------------------------------------------------------#

# ---- [ imports ] ------------------------------------------------------------

import getopt, sys

# ---- [ globals ] ------------------------------------------------------------

debug = False
outputfile = "proj3_grp3.txt"
benchmarkfile = "benchmarks.csv"

# ---- [ classes ] ------------------------------------------------------------

class Grid():
  def __init__(self, inputfile):
    with open(inputfile) as f:
      arr = f.readlines()
      self.num_rows = int(arr[0])
      self.num_cols = int(arr[1])
      self.values = []
      for row in arr[2:]:
        self.values.append(map(lambda x: int(x), row.split(" ")))

  def h_value(self, h, i, j):
    if i < 0 or j < 0:
      return 0
    return h[i][j]

  def heuristic(self):
    h = [[0 for x in range(self.num_rows)] for x in range(self.num_cols)]
    for y in range(0, self.num_rows):
      for x in range(0, self.num_cols):
        h[x][y] = self.values[x][y] + max(self.h_value(h, x-1, y),
          self.h_value(h, x, y-1), 0)
    self.h = h

  def ending_point(self):
    (i, j) = (0, 0)
    val = 0
    for x in range(0, self.num_cols):
      if self.h[x][self.num_rows - 1] > val:
        (i, j) = (x, self.num_cols - 1)
        val = self.h[x][self.num_rows - 1]
    for y in range(0, self.num_rows - 1):
      if self.h[self.num_cols - 1][y] > val:
        (i, j) = (self.num_rows - 1, y)
        val = self.h[self.num_rows - 1][y]
    return (i, j, val)

  def optimal_path(self):
    (x, y, val) = self.ending_point()
    path = [(x,y)]
    while x != 0 and y != 0 and not(self.h[x-1][y] < 0 and self.h[x][y-1] < 0):
      if self.h[x-1][y] > self.h[x][y-1] and x > 0:
        x -= 1
        path.append((x, y))
      else:
        y -= 1
        path.append((x, y))
    return path[::-1]

# ---- [ utility functions ] --------------------------------------------------

def handle_error(message):
  print "Error: {0}".format(message)
  sys.exit(2)

def debug_message(message):
  global debug
  if debug:
    print message

# ---- [ main ] ---------------------------------------------------------------

def main(argv):
  global debug, outputfile, benchmarkfile

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:d',
      ['inputfile=', 'outputfile=', 'debug'])
  except getopt.GetoptError as err:
    handle_error(str(err))

  inputfile = "test.txt"

  for o, a in opts:
    if o in ['-i', '--inputfile']:
      inputfile = a
    elif o in ['-o', '--outputfile']:
      outputfile = a
    elif o in ['-d', '--debug']:
      debug = True
    else:
      handle_error("unhandled option '{0}' detected".format(o))

  # create results output file
  try:
    f = open(outputfile, "w+")
    f.close()
  except IOError:
    handle_error("failed to write to file, '{0}'."
      .format(benchmarkfile))

  # TODO - parse input file
  grid = Grid(inputfile)
  grid.heuristic()
  print grid.optimal_path()

if __name__ == "__main__":
    main(sys.argv[1:])
