import re

line_regex = re.compile(r'position=<(\s?-?\d+), (\s?-?\d+)> velocity=<(\s?-?\d+), (\s?-?\d+)>')




def parse_line(line):
  match = line_regex.match(line)
  if match:
    x = match.group(1)
    y = match.group(2)
    vx = match.group(3)
    vy = match.group(4)
    return int(x), int(y), int(vx), int(vy)


def read_input(path):
  points = []
  with open(path) as file:
    for line in file:
      points.append(parse_line(line))
  return points


def advance(points):
  for ind in range(0, len(points)):
    point = points[ind]
    new_x = point[0] + point[2]
    new_y = point[1] + point[3]
    points[ind] = (new_x, new_y, point[2], point[3])

def sum_distance(points, num_inner):
  tot_dist = 0

  for i in range(0, len(points)):
    p1 = points[i]
    for j in range(0, num_inner):
      p2 = points[j]
      dist = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
      tot_dist = tot_dist + dist
  return tot_dist

def plot_grid(points, min_x, max_x, min_y, max_y):
  grid = []

  # make . grid
  for y in range(min_y, max_y+1):
    next_list = []
    for x in range(min_x, max_x+1):
      next_list.append('.')
    grid.append(next_list)

  # add points
  for point in points:
    grid[point[1]-min_y][point[0]-min_x] = '*'
  
  # print
  for array in grid:
    print(''.join(array))

def main():
  infile = './input/input.dat'
  points = read_input(infile)  

  min_x = min(points, key=lambda x: x[0])[0]
  max_x = max(points, key=lambda x: x[0])[0]
  min_y = min(points, key=lambda x: x[1])[1]
  max_y = max(points, key=lambda x: x[1])[1]

  dist = []
  #for i in range(1,20000):
  #  advance(points)
  #  dist.append(sum_distance(points, 10))
  
  #min_dist, time = min((val, idx) for (idx, val) in enumerate(dist))  
  #print("min dist after {} seconds".format(time))

  time = 10105
  # now replay and print points
  points = read_input(infile)
  for i in range(0,time):
    advance(points)

  with open('output.dat', 'w') as outfile:
    outfile.write('[')    
    for point in points:
      outfile.write('{}, {}; '.format(point[0], point[1]))
    outfile.write(']')

  # copied output into octave online as
  # pts = {output in file}
  # axis equal
  # axis ij
  # plot(pts(:,1), pts(:,2), '.')

if __name__== "__main__":
  main()
