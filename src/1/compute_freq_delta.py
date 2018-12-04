#
# Day 1 of the Advent of Code
# https://adventofcode.com/2018/day/1
#
# part 1) From a list of frequency deltas df_i, compute the final frequency f = sum(df_i)
# part 2) Find the first repeated frequency, repeating the same delta sequence
#

def read_input(file_path):
### open file and read deltas
  deltas = []
  with open(file_path) as in_file:
    for line in in_file:
      deltas.append(int(line))
    return deltas


def delta_loop(frequency, deltas, frequency_history, look_for_first_duplicate=False):
### loop over all deltas to find final frequency
#   If first duplicate is found, print it out
#   return final frequency

  for delta in deltas:
    frequency = frequency + delta
    if look_for_first_duplicate and frequency in frequency_history:
      look_for_first_duplicate = False
      print("Found first duplicate frequency:", frequency)
    frequency_history.add(frequency)
  return frequency, look_for_first_duplicate


def main():
  # read the input
  deltas = read_input('./input/delta_freq.dat')

  # initialize running frequency value and history set
  frequency = 0
  frequency_history = set()
  frequency_history.add(frequency)
  look_for_first_duplicate = True

  # do the first loop
  frequency, look_for_first_duplicate = delta_loop(frequency, deltas, frequency_history, look_for_first_duplicate)
  print("The final frequency after the first loop is:", frequency)

  # continue to loop until first duplicate is found
  while look_for_first_duplicate:
    frequency, look_for_first_duplicate = delta_loop(frequency, deltas, frequency_history, look_for_first_duplicate)
  

if __name__== "__main__":
  main()
