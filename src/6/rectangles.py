#
# Day 6 of the Advent of Code
# https://adventofcode.com/2018/day/4
#
# part 1: find largest non-infinite area in grid 
#
# part 2: 
#

import re

coord_regex = re.compile(r'(\d+), (\d+)')

def read_input(file_path):
  coords = []
  with open(file_path) as in_file:
    for line in in_file:
      match = coord_regex.match(line)
      if match:
        coords.append((int(match.groups()[0]), int(match.groups()[1])))
  return coords


def l1_dist(p1, p2):
  return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def on_boundary(point, boundary):
  return point[0] == boundary[0] or point[0] == boundary[1] or point[1] == boundary[2] or point[1] == boundary[3]


def find_bbox(coords):
  x_min = min(coords, key=lambda x: x[0])[0]
  x_max = max(coords, key=lambda x: x[0])[0]
  y_min = min(coords, key=lambda x: x[1])[1]
  y_max = max(coords, key=lambda x: x[1])[1]
  return (x_min, x_max, y_min, y_max)  

def part_1(coords):
  # find bounding box
  bbox = find_bbox(coords)

  # loop over all points in grid to determine distance from all points in list
  closest_coord = {}  
  grid = [(x,y) for x in range(bbox[0], bbox[1]+1) for y in range(bbox[2], bbox[3]+1)]
  for point in grid:
    min_dist = 100000
    for coord in coords:
      dist = l1_dist(point, coord)
      if dist == min_dist:
        closest_coord[point].append(coord)
      if dist < min_dist:
        min_dist = dist
        closest_coord[point] = [coord]  

  # discard points that have more than one coord the same distance away
  closest_coord = {point: closest_coord[point][0] for point in grid if len(closest_coord[point]) == 1}
  valid_grid = closest_coord.keys() 

  # discard coords on the boundary: they have infinite extent
  infinite_coords = set([closest_coord[point] for point in valid_grid if on_boundary(point, bbox)])
  candidate_points = [point for point in valid_grid if closest_coord[point] not in infinite_coords]
  areas = {coord: 0 for coord in coords}
  for point in candidate_points:
    closest = closest_coord[point] 
    areas[closest] = areas[closest] + 1    

  biggest_non_inifite_area = max(coords, key=lambda x: areas[x])
  print("part 1:", biggest_non_inifite_area, areas[biggest_non_inifite_area])
  

def part_2(coords):
  # find bounding box
  bbox = find_bbox(coords)

  # loop over all points in grid to determine distance from all points in list
  closest_coord = {}  
  grid = [(x,y) for x in range(bbox[0], bbox[1]+1) for y in range(bbox[2], bbox[3]+1)]
  dists = {point: 0 for point in grid}
  for point in grid:
    min_dist = 100000
    for coord in coords:
      dists[point] = dists[point] + l1_dist(point, coord)

  less_than_10000_points = [point for point in grid if dists[point] < 10000]
  print("part 2:", len(less_than_10000_points))



def main():
  coords = read_input('./input/areas.dat')
  #coords = [(0,0), (5,0), (0,5), (5,5), (0,2), (2,0), (2,5), (5,2), (2,2)]

  part_1(coords)
  part_2(coords)

  


if __name__== "__main__":
  main()
