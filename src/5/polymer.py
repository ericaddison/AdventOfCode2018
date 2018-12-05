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


def main():
  polymer_string = read_input('./input/polymer.dat')
  
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
   
  print(len(polymer_string))

if __name__== "__main__":
  main()
