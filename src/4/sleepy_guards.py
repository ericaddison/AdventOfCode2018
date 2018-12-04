#
# Day 4 of the Advent of Code
# https://adventofcode.com/2018/day/4
#
# part 1: find the guard who spent the most time asleep
#
# part 2: find the guard who spent one minute asleep the most
#

import re
import pprint as pp
from enum import Enum

log_regex = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)')
start_shift_regex = re.compile(r'Guard #(\d+) begins shift')

class Event(Enum):
  STARTS_SHIFT = 1
  FALLS_ASLEEP = 2
  WAKES_UP = 3

  def parse(string):
    if string == "wakes up":
      return Event.WAKES_UP, ""
    if string == "falls asleep":
      return Event.FALLS_ASLEEP, ""
    match = start_shift_regex.match(string)
    if match:
      return Event.STARTS_SHIFT, match.group(1)

class GuardSleepLogEntry:
  """An entry in the guard sleep log"""
  def __init__(self, time_info, event, id, log_string):
    self.year = int(time_info[0])
    self.month = int(time_info[1])
    self.day = int(time_info[2])
    self.hour = int(time_info[3])
    self.minute = int(time_info[4])
    self.event = event
    self.id = id
    self.log_string = log_string

  def parse(log_string):
    match = log_regex.match(log_string)
    if match:
      time_info = match.groups()[:5]
      event, id = Event.parse(match.groups()[5])
      return GuardSleepLogEntry(time_info, event, id, log_string)

  def __str__(self):
    return self.log_string

  def __repr__(self):
    return self.log_string
      

def read_input(file_path):
  log_entries = []
  with open(file_path) as in_file:
    for line in in_file:
      log_entries.append(GuardSleepLogEntry.parse(line.strip()))
  return log_entries


def main():
  log_entries = read_input('./input/guard_logs.dat')
  log_entries = sorted(log_entries, key=lambda e: (e.year, e.month, e.day, e.hour, e.minute))

  current_guard_id = -1
  guard_asleep_time = {}
  guard_sleep_map = {}

  # build map of maps with guard sleep times
  for log in log_entries:

    if log.event == Event.STARTS_SHIFT:
      current_guard_id = log.id

    if log.event == Event.FALLS_ASLEEP:
      guard_asleep_time[current_guard_id] = log.minute

    if log.event == Event.WAKES_UP:
      for minute in range(guard_asleep_time[current_guard_id], log.minute):
        if current_guard_id in guard_sleep_map.keys():
          guard_map = guard_sleep_map[current_guard_id]
          if minute in guard_map.keys():
            guard_map[minute] = guard_map[minute] + 1
          else:
            guard_map[minute] = 1
        else:
          guard_sleep_map[current_guard_id] = {minute: 1}
        
  # find guard with most time asleep
  sleepiest = ("none", -1)
  for guard, sleep_map in guard_sleep_map.items():
    time_asleep = sum([num_minutes for num_minutes in sleep_map.values()])
    if time_asleep > sleepiest[1]:
      sleepiest = (guard, time_asleep)

  # part 1: find the guard who spent the most time asleep
  print("(sleepiest guard, time slept):", sleepiest)
  sleepiest_minute = max(guard_sleep_map[sleepiest[0]].items(), key=lambda x: x[1])
  print("sleepiest minute:", sleepiest_minute[0])
  print("product:", (sleepiest_minute[0]*int(sleepiest[0])))

  # part 2: find the guard who spent one minute asleep the most
  most_sleep_minute = ("none", 0, -1)
  for guard, sleep_map in guard_sleep_map.items():
    sleepiest_minute = max(guard_sleep_map[guard].items(), key=lambda x: x[1])
    if sleepiest_minute[1] > most_sleep_minute[2]:
      most_sleep_minute = (guard, sleepiest_minute[0], sleepiest_minute[1])

  print("\nThe minute that a guard was most frequently asleep on was:", most_sleep_minute[1]);
  print("The guard was:", most_sleep_minute[0]);
  print("The product is:", int(most_sleep_minute[0])*most_sleep_minute[1]);

if __name__== "__main__":
  main()
