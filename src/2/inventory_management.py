

def read_input(file_path):
### open file and read ids
  ids = []
  with open(file_path) as in_file:
    for line in in_file:
      ids.append(line)
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


def main():
  file_path = './input/ids.dat'
  ids = read_input(file_path)
  print("The checksum is:", checksum(ids))

if __name__== "__main__":
  main()
