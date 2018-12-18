import re

entry_regex = re.compile(r'Step (.{1}) must be finished before step (.{1}) can begin.')


def read_input(path):
  entries = {}
  with open(path) as infile:
    for line in infile:
      match = entry_regex.match(line)
      happens_before = match.groups()[0]
      step = match.groups()[1]
      if step not in entries.keys():
        entries[step] = []
      if happens_before not in entries.keys():
        entries[happens_before] = []
      entries[step].append(happens_before)
  return entries        


def timer(task, base_time):
  return base_time + (ord(task) - 64)

def main():
  # read input
  infile = './input/input.dat'
  entries = read_input(infile)
  print('read number of distinct entries:', len(entries))

  # part 1
  roots = sorted([e for e in entries if not entries[e]])
  to_do = roots[:]
  order = []

  while to_do:
    task = to_do.pop(0)
    order.append(task)
    successors = [e for e in entries if task in entries[e]]
    for successor in successors:
      entries[successor].remove(task)
      if not entries[successor]:
        to_do.append(successor)
    to_do = sorted(to_do)
    #print('to_do:', to_do)

  print("".join(order))

  # part 2
  infile = './input/input.dat'
  entries = read_input(infile)

  roots = sorted([e for e in entries if not entries[e]])
  to_do = roots[:]

  time_per_task = 60
  num_elves = 5
  elf_tasks = {}
  for elf in range(num_elves):
    elf_tasks[elf] = None
  done = []  

  t = 0
  while True:
    # decrement elf task timers
    for elf in range(num_elves):
      task = elf_tasks[elf]
      if task:
        task[1] -= 1
        if task[1] == 0:  # if task is done
          done.append(task[0])
          elf_tasks[elf] = None
          successors = [e for e in entries if task[0] in entries[e]]
          for successor in successors:
            entries[successor].remove(task[0])
            if not entries[successor]:
              to_do.append(successor)

    # assign new tasks
    free_elves = [elf for elf in range(num_elves) if not elf_tasks[elf]]
    while len(free_elves)>0 and len(to_do)>0:
      task = to_do.pop(0)
      free_elf = free_elves.pop(0)
      elf_tasks[free_elf] = [task, timer(task, time_per_task)]
    to_do = sorted(to_do)

    s = [str(t)]
    for elf in range(num_elves):
      task = elf_tasks[elf]
      s.append(task[0] if task else '.')
    s.append("".join(done))
    print("   ".join(s))

    if len(done) == len(entries):
      break

    t += 1
      
  print('took seconds:', t)    

if __name__== "__main__":
  main()
