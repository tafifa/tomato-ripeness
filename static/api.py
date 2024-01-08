import sys
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

module_path = os.path.join(module_dir, '..', 'python')

sys.path.insert(0, module_path)

import DistanceComparator as dco

dc = dco.DistanceComparator()

def call(path):
  pathTest = path
  metric = 'canberra'

  # res = 15

  matang, mentah = dc.distanceComparison(pathTest, metric)

  res = 1 if matang > mentah else 0

  return res

if __name__ == "__main__":
  print(call(r'..\static\temp\*'))
