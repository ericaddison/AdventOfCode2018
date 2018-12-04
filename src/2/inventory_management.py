#
# Day 2 of the Advent of Code
# https://adventofcode.com/2018/day/2
#
# part 1) From a list of inventory ids, compute a checksum as: 
#   (number of ids with a character repeated twice) * (number of ids with a character repeated three times)
#
# part 2) Find the two IDs with exactly one differing character
#


def read_input(file_path):
### open file and read ids
  ids = []
  with open(file_path) as in_file:
    for line in in_file:
      ids.append(line.strip())
    return ids


def char_counts(in_string):
  char_count = {}
  for char in in_string:
    current_count = char_count.get(char, 0)
    char_count[char] = current_count + 1
  return char_count


def checksum(ids):
  two_char_id_count = 0
  three_char_id_count = 0

  for id in ids:
    char_count = char_counts(id)
    if 2 in char_count.values():
      two_char_id_count = two_char_id_count + 1
    if 3 in char_count.values():
      three_char_id_count = three_char_id_count + 1

  return two_char_id_count * three_char_id_count


def id_sum(id):
  char_vals = [ord(c) for c in id]
  return sum(char_vals)

  
def differs_by_one(id1, id2):
  differs = [c1!=c2 for (c1,c2) in zip(id1,id2)]  
  if sum(differs) == 1:
    return differs.index(True)
  return -1


def find_ids_that_differ_by_one_char(ids):
  id_and_sum = sorted([(id, id_sum(id)) for id in ids], key=lambda x: x[1])

  for (id1, id_sum1) in id_and_sum:
    for(id2, id_sum2) in id_and_sum:
      if id1 == id2: continue

      # if sum differs by more than 26, must differ by more than one char
      if id_sum1 - id_sum2 > 26:
        continue
      if id_sum2 - id_sum1 > 26:
        break
      differ_index = differs_by_one(id1, id2)
      if differ_index > -1:
        return (id1, id2, differ_index)


def main():
  file_path = './input/ids.dat'
  ids = read_input(file_path)
  print("The checksum is:", checksum(ids))
  
  id1, id2, differ_index = find_ids_that_differ_by_one_char(ids)
  print("{} and {} differ at index {}".format(id1, id2, differ_index))
  print("Common characters: {}{}".format(id1[:differ_index], id1[differ_index+1:]))
      

if __name__== "__main__":
  main()
