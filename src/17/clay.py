import re

clay_regex = re.compile(r'([xy])=(\d+), [xy]=(\d+)..(\d+)')
found_wall_regex = re.compile(r'found_wall\((\d+), (\d+)\)')

# location of the water spring
spring_loc = (500, 0)

# messages passed in the loop
flow = 'flow'
found_wall = 'found_wall'
rest = 'rest'
spread = 'spread'

# types of squares
empty = '.'
clay = '#'
rest_water = '~'
knows_about_wall = '!'
flow_water = '|'
spring = '+'
  
flowing_water_list = [knows_about_wall, flow_water]
item_list = [empty, clay, rest_water, flow_water, spring, knows_about_wall]

def print_board(items, active=None):
  coords = items.keys()
  xs = [c[0] for c in coords]
  ys = [c[1] for c in coords]
  xmin = min(xs)
  xmax = max(xs)
  ymin = min(ys)
  ymax = max(ys)

  for y in range(ymin-1, ymax+2):
    next_line = []
    for x in range(xmin-1, xmax+2):
      if (x,y)==active:
        next_line.append('*')
      elif (x,y) in coords:
        next_line.append(items[(x,y)])
      else:
        next_line.append(empty)
    print("".join(next_line))


def write_board(items):
  coords = items.keys()
  xs = [c[0] for c in coords]
  ys = [c[1] for c in coords]
  xmin = min(xs)
  xmax = max(xs)
  ymin = min(ys)
  ymax = max(ys)

  with open('./out/map.dat', 'w') as outfile:
    for y in range(ymin-1, ymax+2):
      for x in range(xmin-1, xmax+2):
        if (x,y) in coords:
          outfile.write(str(item_list.index(items[(x,y)])) + ', ')
        else:
          outfile.write(str(item_list.index(empty)) + ', ')
      outfile.write('\n')


def read_input(path):
  clay_coords = {}
  with open(path) as infile:
    for line in infile:
      match = clay_regex.match(line)
      static_coord = int(match.groups()[1])
      range_1 = int(match.groups()[2])
      range_2 = int(match.groups()[3])
      if match.groups()[0] == 'x':
        x = static_coord
        for y in range(range_1, range_2+1):
          clay_coords[(x, y)] = clay
      else:
        y = static_coord
        for x in range(range_1, range_2+1):
          clay_coords[(x, y)] = clay
  return clay_coords


def add_tuples(t1, t2):
  return (t1[0]+t2[0], t1[1]+t2[1])


def sub_tuples(t1, t2):
  return (t1[0]-t2[0], t1[1]-t2[1])


def is_flowing(item):
  return item in flowing_water_list

def main():
  # read input
  infile = './input/input.dat'
  items = read_input(infile)
  max_clay_y = max(items.keys(), key=lambda p: p[1])[1]
  min_clay_y = min(items.keys(), key=lambda p: p[1])[1]
  print('Input', len(items), 'clay coordinates from', infile)
  print('max y:', max_clay_y)
  print('min y:', min_clay_y)

  # add water source
  items[spring_loc] = spring
  
  # prepare for loop
  action_Q = [(add_tuples(spring_loc, (0, 1)), flow, spring_loc)]
  water_reachable = set()

  cnt = 0
  while action_Q:
  #for i in range(60316):
    cnt += 1
    active_coord, action, from_coord = action_Q.pop(0)
    item = items.get(active_coord, empty)
    if item == clay:
      print("ERROR!!!")
      break
    if active_coord[1] > max_clay_y:
      continue
    
    if active_coord[1] >= min_clay_y: 
      water_reachable.add(active_coord)

    #print('\n', cnt, ':', active_coord, action)
    #print_board(items, active_coord)

    below = add_tuples(active_coord, (0, 1))
    below_item = items.get(below, empty)
    above = add_tuples(active_coord, (0, -1))
    above_item = items.get(above, empty)
    left = add_tuples(active_coord, (-1, 0))
    left_item = items.get(left, empty)
    right = add_tuples(active_coord, (1, 0))
    right_item = items.get(right, empty)

    if action == flow:
      items[active_coord] = flow_water
      if below_item == empty:
        action_Q.append((below, flow, active_coord))
      elif is_flowing(below_item):
        continue
      else:
        action_Q.append((active_coord, spread, active_coord))
    
    elif action == spread:
      items[active_coord] = flow_water

      if below_item == empty:
        action_Q.append((active_coord, flow, active_coord))
        continue
  
      # if can spread into empty space
      if left_item == empty:
        action_Q.append((left, spread, active_coord))
      if right_item == empty:
        action_Q.append((right, spread, active_coord))

      # if found a wall on one side and other side is flowing
      if left_item == clay and is_flowing(right_item):
        action_Q.append((active_coord, found_wall, active_coord))
      if right_item == clay and is_flowing(left_item):
        action_Q.append((active_coord, found_wall, active_coord))

      # if found two walls
      if right_item == clay and left_item == clay:
        action_Q.append((active_coord, rest, active_coord))

      # if spreading and found already-known wall water
      if from_coord == left and right_item == knows_about_wall:
        action_Q.append((active_coord, found_wall, active_coord))
      if from_coord == right and left_item == knows_about_wall:
        action_Q.append((active_coord, found_wall, active_coord))

    elif action == found_wall and item != knows_about_wall:
      items[active_coord] = knows_about_wall
      # if you were told that a wall was found, but it wasn't your wall, then come to rest
      if left_item == knows_about_wall and right_item == clay:
        action_Q.append((active_coord, rest, active_coord))
      elif right_item == knows_about_wall and left_item == clay:  
        action_Q.append((active_coord, rest, active_coord))
      elif right_item == knows_about_wall and left_item == knows_about_wall:
        action_Q.append((active_coord, rest, active_coord))
      # else pass the found_wall message to the next in line
      else:
        if right_item == flow_water:
          action_Q.append((right, found_wall, active_coord))
        if left_item == flow_water:
          action_Q.append((left, found_wall, active_coord))

    elif action == rest:
      items[active_coord] = rest_water
      if is_flowing(left_item):
        action_Q.append((left, rest, active_coord))
      if is_flowing(right_item):
        action_Q.append((right, rest, active_coord))
      if is_flowing(above_item):
        action_Q.append((above, spread, active_coord))
              
  print('\n')
  write_board(items)
  

  num_rest_water = len([c for c in items.values() if c == rest_water])
  print('found number of water spaces:', len(water_reachable))
  print('took number of turns', cnt)
  print('amount of at rest water:', num_rest_water)
  
if __name__== "__main__":
  main()
