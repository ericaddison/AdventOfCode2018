
goblin_char = 'G'
elf_char = 'E'
wall_char = '#'
empty_char = '.'
directions = [(-1,0), (0,-1), (0, 1), (1,0)]


def read_input(path):
  walls = []
  players = []
  the_map = []
  with open(path) as file:
    row = 0
    for line in file:
      col = 0
      for c in line:
        if c == wall_char:
          walls.append((row, col))
        if c == goblin_char:
          players.append([(row, col), goblin_char])
        elif c == elf_char:
          players.append([(row, col), elf_char])
        col += 1
      the_map.append([c for c in line if c != '\n'])
      row += 1
  return the_map, walls, players


def find_in_range_spaces(the_map, enemies, my_loc):
  in_range_map = {}         # key = open map location, value = enemy location
  for enemy_loc in enemies:
    for direction in directions:
      adjacent = add_tuples(enemy_loc, direction)
      map_char = the_map[adjacent[0]][adjacent[1]]
      if map_char == empty_char or adjacent == my_loc:
        in_range_map[adjacent] = enemy_loc
  return in_range_map


def find_path_to_closest_in_range_space(the_map, my_loc, in_range_spaces):
  """ find the shortest distance to all in-range locations from my_loc"""  
  to_visit = [(my_loc, [])]
  visited = {}
  while len(to_visit) > 0:
    loc, path = to_visit.pop(0)
    if loc in in_range_spaces:
      return path
    visited[loc] = path
    for d in directions:
      next_space = add_tuples(loc, d)
      map_char = the_map[next_space[0]][next_space[1]]
      if next_space not in visited.keys() and map_char == empty_char:
        next_space_path = path[:]
        next_space_path.append(next_space)
        to_visit.append((next_space, next_space_path))
  return None


def add_tuples(t1, t2):
  return (t1[0]+t2[0], t1[1]+t2[1])


def get_enemy_locations(players, enemy_type):
  return [player[0] for player in players if player[1] == enemy_type]


def move_player(player, move, the_map):
  player_loc = player[0]
  the_map[player_loc[0]][player_loc[1]] = '.'
  the_map[move[0]][move[1]] = player[1]
  player[0] = move


def print_map(the_map):
  for i in range(len(the_map)):
    print("".join(the_map[i]))


def do_round(the_map, players):
  print('\n-------- new round ----------')
  # sort by 'reading' order
  players = sorted(players, key=lambda p: p[0])

  # loop through all players
  for player in players:
    print('starting turn for player', player)
    loc = player[0]
    player_type = player[1]
    if player_type == elf_char:
      enemies = get_enemy_locations(players, goblin_char)
    else:
      enemies = get_enemy_locations(players, elf_char)

    print('-- enemy locations: ', enemies)

    in_range_spaces = find_in_range_spaces(the_map, enemies, loc)
    print('-- in range spaces ', in_range_spaces)
    in_range = loc in in_range_spaces.keys()
    print('-- in range? ', in_range)

    if in_range: #attack!
      pass
    else: #move!
      shortest_path = find_path_to_closest_in_range_space(the_map, loc, in_range_spaces)
      print('shortest path ', shortest_path)
      next_move = shortest_path[0] if shortest_path else loc
      print('-- moving to ', next_move)
      move_player(player, next_move, the_map)     


def main():
  infile = './input/test_map.dat'
  the_map, walls, players = read_input(infile)
  print_map(the_map)
  do_round(the_map, players)  
  print_map(the_map)
  do_round(the_map, players)  
  print_map(the_map)
  do_round(the_map, players)  
  print_map(the_map)
  print(players)

  #in_range_gobs = find_in_range_spaces(the_map, goblins)
  #in_range_elves = find_in_range_spaces(the_map, elves)
  #print(find_path_to_closest_in_range_space(the_map, elves[0], in_range_gobs))

if __name__== "__main__":
  main()
