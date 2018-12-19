def char_count(char, char_list):
  return len([c for c in char_list if c==char])


def open_rule(adjacent): 
  return '|' if char_count('|', adjacent)>=3 else '.'
def tree_rule(adjacent): 
  return '#' if char_count('#', adjacent)>=3 else '|'
def lumberyard_rule(adjacent):
  return '#' if char_count('|', adjacent)>=1 and char_count('#', adjacent)>=1 else '.' 
rules = {'.': open_rule, '|': tree_rule, '#': lumberyard_rule}


def tick(the_map):
  rows = len(the_map)
  cols = len(the_map[0])
  padded_map = ['.'*(cols+2)] + ['.'+line+'.' for line in the_map] + ['.'*(cols+2)]
  new_chars = [[apply_rules(r+1, c+1, padded_map) for c in range(cols)] for r in range(rows)]
  return ["".join(row) for row in new_chars]

  
def apply_rules(row, col, the_map):
  adjacent = [the_map[row+r][col+c] for r in [-1, 0, 1] for c in [-1, 0, 1]]
  return rules[adjacent.pop(4)](adjacent) 


def result(the_map):
  num_trees = len([c for line in the_map for c in line if c=='|'])
  num_yards = len([c for line in the_map for c in line if c=='#'])
  return num_trees*num_yards

  
def main():
  infile = './input/input.dat'
  orig_map = [line.strip() for line in open(infile)]

  # part 1
  the_map = orig_map[:]
  for i in range(10):
    the_map = tick(the_map)
  print('part 1:', result(the_map))

  # part 2
  the_map = orig_map[:]
  maps = [the_map]
  for i in range(500):
    the_map = tick(the_map)
    if the_map in maps:
      repeat_time = i
      previous_time = maps.index(the_map)
      print('found dup at times', i, 'and', previous_time)
      break
    maps.append(the_map)

  # repeat starts at time  previous_time with interval repeat_interval
  # so 10000000000 = previous_time + x + y*repeat_interval
  # and then the map = maps[previous_time + x]
  # where x = (10000000000-previous_time)%repeat_interval
  interval = repeat_time - previous_time + 1
  print('found repeat interval', interval)
  desired_time = 1000000000
  x = (desired_time-previous_time)%interval
  print('part 2:', result(maps[previous_time+x]))


if __name__== "__main__":
  main()
