

def get_rack_id(x):
  return x + 10


def power_level(x, y, grid_serial):
  rack_id = get_rack_id(x)
  return (((((rack_id * y) + grid_serial) * rack_id) // 100) % 10) - 5

def total_power_dynamic(x, y, size, power_table):
  tot_pow = power_table[(x, y, size-1)]
  for ix in range(x, x+size):
    tot_pow = tot_pow + power_table[(ix, y+size-1, 1)]

  for iy in range(y, y+size-1):
    tot_pow = tot_pow + power_table[(x+size-1, iy, 1)]

  return tot_pow

def main():
  grid_serial = 6392
  max_power_level = -1000000
  max_corner = (-1, -1, -1)
  grid_size = 300
  powers = {(x, y, 1) : power_level(x, y, grid_serial) for x in range(1, grid_size+1) for y in range(1, grid_size+1)}

  for size in range(2, grid_size+1):
    for y in range(1, grid_size-size+1):
      for x in range(1, grid_size-size+1):
        power = total_power_dynamic(x, y, size, powers)
        powers[(x, y, size)] = power
        if power > max_power_level:
          max_power_level = power
          max_corner = (x, y, size)
    print("size {}: max = {}".format(size, max_corner))

  print("top left of max_coord: ", max_corner)


if __name__== "__main__":
  main()
