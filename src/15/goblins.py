
goblin_char = 'G'
elf_char = 'E'
wall_char = '#'
empty_char = '.'
directions = [(-1,0), (0,-1), (0, 1), (1,0)]


class Player:
  def __init__(self, loc, team, hp, ap):
    self.loc = loc
    self.team = team
    self.hp = hp    # hit points
    self.ap = ap    # attack power
    self.alive = True

  def move_to(self, new_loc):
    self.loc = new_loc

  def attack(self, target):
    target.hp -= self.ap
    if target.hp <= 0:
      target.alive = False

  def __str__(self):
    return self.team + '[' + str(self.loc) + ', ' + str(self.hp) + ']'

  def __repr__(self):
    return self.team + '[' + str(self.loc) + ', ' + str(self.hp) + ']'
    #return self.team + '(' + str(self.hp) + ')'


def read_input(path, elf_ap=3):
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
          players.append(Player((row, col), goblin_char, 200, 3))
        elif c == elf_char:
          players.append(Player((row, col), elf_char, 200, elf_ap))
        col += 1
      the_map.append([c for c in line if c != '\n'])
      row += 1
  return the_map, walls, players


def log(*args):
  if logging:
    print(*args)

def find_in_range_spaces(the_map, enemies):
  in_range_map = {}         # key = open map location, value = enemy location
  for enemy in enemies:
    for direction in directions:
      adjacent = add_tuples(enemy.loc, direction)
      map_char = the_map[adjacent[0]][adjacent[1]]
      if map_char == empty_char:
        in_range_map[adjacent] = enemy.loc
  return in_range_map


def is_adjacent(loc1, loc2):
  return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1]) == 1


def find_adjacent_enemies(player, enemies):
  return [enemy for enemy in enemies if is_adjacent(player.loc, enemy.loc)]    


def find_path_to_closest_in_range_space(the_map, player, in_range_spaces):
  """ find the shortest distance to all in-range locations from my_loc"""  
  to_visit = [player.loc]
  paths = {player.loc: []}
  shortest_paths = []
  visited = set()
  while len(to_visit) > 0:
    loc = to_visit.pop(0)
    path = paths[loc]
    if loc in in_range_spaces.keys():
      if not shortest_paths or len(path) == len(shortest_paths[0]):
        shortest_paths.append(path)
    visited.add(loc)
    for d in directions:
      next_space = add_tuples(loc, d)
      map_char = the_map[next_space[0]][next_space[1]]
      if map_char == empty_char and next_space not in visited and next_space not in to_visit:
        next_space_path = path[:]
        next_space_path.append(next_space)
        to_visit.append(next_space)
        paths[next_space] = next_space_path
    # here was my big problem! I wasn't waiting to check for multiple shortest paths!!!
    # my idea of relying on the direction order was BAD
    if shortest_paths:
      if not to_visit or min([len(paths[loc]) for loc in to_visit]) > len(shortest_paths[0]):
        return min(shortest_paths, key=lambda p: p[-1:])
  return None


def add_tuples(t1, t2):
  return (t1[0]+t2[0], t1[1]+t2[1])


def get_enemy_locations(players, enemy_type):
  return [player.loc for player in players if player.team == enemy_type]


def move_player(player, move, the_map):
  the_map[player.loc[0]][player.loc[1]] = '.'
  the_map[move[0]][move[1]] = player.team
  player.move_to(move)


def print_map(the_map, players, force_print=False):
  if not logmap and not force_print:
    return
  for row in range(len(the_map)):
    players_this_row = sorted([p for p in players if p.loc[0] == row and p.alive], key=lambda p: p.loc[1]) 
    print("".join(the_map[row]), players_this_row)
  print('\n')


def write_map_csv(the_map, path):
  if not writemap:
    return
  with open(path, 'w') as file:
    for row in the_map:
      for c in row:
        if c == wall_char:
          file.write('0')
        elif c == empty_char:
          file.write('1')
        elif c == elf_char:
          file.write('2')
        elif c == goblin_char:
          file.write('3')
        else:
          file.write('999')
        file.write(', ')
      file.write('\n')
    

def attack(player, adjacent_enemies, the_map):
  adjacent_enemies = sorted(adjacent_enemies, key=lambda e: e.hp)  
  lowest_hp = adjacent_enemies[0].hp
  lowest_hp_enemies = [e for e in adjacent_enemies if e.hp == lowest_hp]
  target = sorted(lowest_hp_enemies, key=lambda p: p.loc)[0]
  player.attack(target)
  if not target.alive:
    the_map[target.loc[0]][target.loc[1]] = '.'
    log('--', player, 'Killed ', target)
  else:
    log('--', player, 'Attacked ', target)


def do_round(the_map, players):
  # sort by 'reading' order
  players = sorted(players, key=lambda p: p.loc)

  # loop through all players
  for player in players:
    if not player.alive:
      continue

    log('starting turn for player', player)
    if player.team == elf_char:
      enemies = [e for e in players if e.team == goblin_char and e.alive]
    else:
      enemies = [e for e in players if e.team == elf_char and e.alive]

    if not enemies:
      log('-- GAME OVER!')
      return True

    adjacent_enemies = find_adjacent_enemies(player, enemies)
    in_range = len(adjacent_enemies)>0

    if in_range: #attack!
      attack(player, adjacent_enemies, the_map)
    else: #move!
      in_range_spaces = find_in_range_spaces(the_map, enemies)
      shortest_path = find_path_to_closest_in_range_space(the_map, player, in_range_spaces)
      next_move = shortest_path[0] if shortest_path else player.loc
      if next_move == player.loc:
        log('--', player, 'found no clear path, not moving')
      else:
        log('--', player, 'moving to ', next_move)
        move_player(player, next_move, the_map)

      adjacent_enemies = find_adjacent_enemies(player, enemies)
      in_range = len(adjacent_enemies)>0
      if in_range:
        attack(player, adjacent_enemies, the_map)
    log('--', player, 'turn over')

  return False


def get_result(round, players):
  return round * sum([p.hp for p in players if p.alive])


logging = False
logmap = False
writemap = False


def main():
  infile = './input/map.dat'
  the_map, walls, players = read_input(infile)
  log(' ----- initial ------')
  print_map(the_map, players)
  write_map_csv(the_map, './out/map0')

  # part 1
  round = 0
  while True:
    log(' ----- round', round, ' ------')
    game_over = do_round(the_map, players)
    if game_over:
      break
      
    print_map(the_map, players)
    write_map_csv(the_map, './out/map' + str(round))
    log(players)
    round += 1

  print_map(the_map, players, True)
  print('played', round, 'rounds')
  print('final player hp sum: ', sum([p.hp for p in players if p.alive]))
  result = get_result(round, players)
  print('Battle result:', result)

  # part 2
  elf_ap = 3
  while True:
    elf_ap += 1
    the_map, walls, players = read_input(infile, elf_ap)
    round = 0
    while True:
      log(' ----- round', round, ' ------')
      game_over = do_round(the_map, players)
      if game_over:
        break
        
      print_map(the_map, players)
      write_map_csv(the_map, './out/map' + str(round))
      log(players)
      round += 1  
    print('number of dead elves = ', len([e for e in players if e.team == elf_char and not e.alive]))
    if len([e for e in players if e.team == elf_char and not e.alive]) == 0:
      break

  print('\n\npart 2')
  print_map(the_map, players, True)
  print('elf ap = ', elf_ap)
  print('played', round, 'rounds')
  print('final player hp sum: ', sum([p.hp for p in players if p.alive]))
  result = get_result(round, players)
  print('Battle result:', result)

  
if __name__== "__main__":
  main()
