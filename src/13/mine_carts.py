
directions = ['^', '>', 'v', '<']
backslash_turns = {'^': '<', '<': '^', 'v': '>', '>': 'v'}
forwardslash_turns = {'^': '>', '>': '^', 'v': '<', '<': 'v'}

class Cart:
  def __init__(self, location, direction):
    self.turn_index = 0
    self.location = location
    self.direction = direction

  def intersection_turn(self):
    turn_index = -1 + (self.turn_index%3)
    direction_index = directions.index(self.direction)  
    self.direction = directions[(direction_index+turn_index)%4]
    self.turn_index = self.turn_index + 1


def read_input(path):
  track = []
  carts = []
  with open(path) as infile:
    y = 0
    for line in infile:
      track_line = []
      for x in range(len(line)):
        c = line[x]
        location = (x,y)
        if c in ['<', '>']:
          carts.append(Cart(location,c))
          track_line.append('-')
        elif c in ['v', '^']:
          carts.append(Cart(location,c))
          track_line.append('|')          
        elif c != '\n':
          track_line.append(c)
      track.append(track_line)
      y = y + 1
  return track, carts


def print_track(track, carts):
  y = 0  
  for line in track:
    line_carts = [cart for cart in carts if cart.location[1] == y]
    this_line = [c for c in line]
    for cart in line_carts:
      this_line[cart.location[0]] = cart.direction
    print("".join(this_line))
    y = y + 1


def move_cart(track, cart):
  x = cart.location[0]
  y = cart.location[1]
  current_track = track[y][x]

  print('cart at location {} with direction {} is on a {}'.format(cart.location, cart.direction, current_track))

  # move the cart
  if cart.direction == '^':
    cart.location = (x, y-1)
  elif cart.direction == 'v':
    cart.location = (x, y+1)
  elif cart.direction == '<':
    cart.location = (x-1, y)
  elif cart.direction == '>':
    cart.location = (x+1, y) 

  print('new location is ', cart.location)

  # turn if necessary
  x = cart.location[0]
  y = cart.location[1]
  next_track = track[y][x]
  if next_track == '/':
    cart.direction = forwardslash_turns[cart.direction]

  elif next_track == '\\':
    cart.direction = backslash_turns[cart.direction]

  elif next_track == '+':
    cart.intersection_turn()
      
  print('new track piece is {}, so new direction is {}'.format(next_track, cart.direction))
  print('')

def check_for_collisions(track, cart, all_carts):
  collisions = [c2 for c2 in all_carts if c2!=cart and c2.location == cart.location]
  if len(collisions) > 0:
    return collisions[0].location
  return None   

    
def move_carts(track, carts):
  for cart in carts:
    move_cart(track, cart)  
    collision_location = check_for_collisions(track, cart, carts) 
    if collision_location:
      return collision_location
  return None

def main():
  track, carts = read_input('./input/track.dat')
  #print_track(track, carts)

  tick = 1
  while(True):
    print("TICK ", tick)
    carts = sorted(carts, key=lambda cart: (cart.location[1], cart.location[0]))
    possible_collision_location = move_carts(track, carts)
    if possible_collision_location:
      print("first collision found at location:", possible_collision_location)
      break  
    print("-------------------------\n\n")
    tick = tick + 1
    #print_track(track, carts)
  

if __name__== "__main__":
  main()
