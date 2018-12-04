#
# Day 3 of the Advent of Code
# https://adventofcode.com/2018/day/1
#
# part 1)
#
# part 2)
#

import re

claim_regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)') 

class Claim:
  """A claim on santa's fabric made by an elf"""
  def __init__(self, args):
    self.id = args[0]
    self.left = int(args[1])
    self.top = int(args[2])
    self.width = int(args[3])
    self.height = int(args[4])


def read_input(file_path):
  claims = []
  with open(file_path) as in_file:
    for line in in_file:
      claims.append(parse_claim(line))
  return claims


def parse_claim(claim_string):
  match = claim_regex.match(claim_string)
  if match:
    return Claim(match.groups())


def main():
  claims = read_input('./input/claims.dat')

  claimed_blocks = {}
  conflict_blocks = set()
  no_conflicts = set([claim.id for claim in claims])

  for claim in claims:
    for x in range(claim.left, claim.left+claim.width):
      for y in range(claim.top, claim.top+claim.height):
        block = (x,y)
        if block in claimed_blocks.keys():
          claimed_blocks[block].append(claim.id)
          conflict_blocks.add(block)
          if claim.id in no_conflicts:
            no_conflicts.remove(claim.id)
          if claimed_blocks[block][0] in no_conflicts:
            no_conflicts.remove(claimed_blocks[block][0])
        else:
          claimed_blocks[block] = [claim.id]

  print("Number of square inches in conflict:", len(conflict_blocks))

  print("Claims with no conflicts:", no_conflicts)
      

if __name__== "__main__":
  main()
