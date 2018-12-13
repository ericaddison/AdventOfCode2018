import re

rule_regex = re.compile(r'([\.#]{5}) => ([\.#])')
grid_regex = re.compile(r'initial state: ([\.#]+)')


class Rule:
  def __init__(self, template, alive):
    self.template = template
    self.alive = alive

  def parse(string):
    match = rule_regex.match(string)
    if match:
      template = match.group(1)
      alive = match.group(2)
      return Rule(template, alive)
    return None


def read_input(path):
  init_grid = ''
  rules = []
  with open(path) as infile:
    cnt = 0
    for line in infile:
      if cnt == 0:
        init_grid = grid_regex.match(line).group(1)
      elif cnt > 1:
        rules.append(Rule.parse(line))
      cnt = cnt + 1
  return init_grid, rules


def apply_rule(segment, rule):
  if segment == rule.template:
    return rule.alive
  return None


def advance(grid, rules):
  augmented_grid = "....." + grid + "....."
  grid = ['.' for x in range(0, len(augmented_grid))]
  for pos in range(2, len(augmented_grid)-2):
    for rule in rules:
      result = apply_rule(augmented_grid[pos-2:pos+3], rule)    
      if result:
        grid[pos] = result

  first_hash = grid.index('#')
  last_hash = len(grid) - 1 - grid[::-1].index('#')
  offset_delta = first_hash-5

  return ''.join(grid[first_hash:last_hash+1]), offset_delta


def find_sum(grid, offset):
  sum = 0
  for i in range(0,len(grid)):
    if grid[i] == '#':
      sum = sum + i+offset
  return sum


def main():
  grid, rules = read_input('./input/input.dat')
  offset = 0
  sum = find_sum(grid, offset)
  print(grid)

  for i in range(1, 1000):
    new_grid, offset_delta = advance(grid, rules)
    offset = offset + offset_delta
    new_sum = find_sum(new_grid, offset)
    sum_diff = new_sum - sum
    print(i, ": grid length = ", len(new_grid), " offset = ", offset, " sum = ", new_sum)
    if new_grid == grid:
      print("found repeated grids:")
      break
    grid = new_grid
    sum = new_sum


  target_year = 50000000000

  print("sum at {} = {}".format(target_year, new_sum + sum_diff*(target_year-i)))
  
 

if __name__== "__main__":
  main()
