#
# Day 1 of the Advent of Code
# https://adventofcode.com/2018/day/1
#
# From a list of frequency deltas df_i, compute the final frequency f = sum(df_i)
#

frequency = 0
with open('./input/delta_freq.dat') as in_file:
  for line in in_file:
    frequency = frequency + int(line)

print("The final frequency is:", frequency)
