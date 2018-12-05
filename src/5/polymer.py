#
# Day 5 of the Advent of Code
# https://adventofcode.com/2018/day/4
#
# part 1: remove lower-case:upper-case pairs
#
# part 2: 
#


def read_input(file_path):
  polymer_string = ""
  with open(file_path) as in_file:
    for line in in_file:
      polymer_string = line.strip()
  return polymer_string

def react_polymer(polymer_string):
  had_reaction = True
  while had_reaction:
    had_reaction = False
    polymer_list = list(polymer_string)  
    for i in range(0, len(polymer_list)-1):
      c1 = polymer_list[i]
      c2 = polymer_list[i+1]
      if c1.lower() == c2.lower() and c1 != c2:
        polymer_list[i] = '~'
        polymer_list[i+1] = '~'
        had_reaction = True
    polymer_string = "".join(polymer_list).replace('~', '')
  return polymer_string 


def main():
  polymer_string = read_input('./input/polymer.dat')
 
  # part 1
  reacted_polymer_string = react_polymer(polymer_string)
  print("part 1:", len(reacted_polymer_string))

  # part 2
  min_length = 1000000000
  for c in 'abcdefghijklmnopqrstuvwxyz':
    replaced_polymer = polymer_string.replace(c, '').replace(c.upper(), '')
    reacted_replaced_polymer = react_polymer(replaced_polymer)
    if len(reacted_replaced_polymer) < min_length:
      min_length = len(reacted_replaced_polymer)

  print("part 2:", min_length)

if __name__== "__main__":
  main()
