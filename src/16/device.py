import re

before_regex = re.compile(r'Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]')
instr_regex = re.compile(r'(\d+) (\d+) (\d+) (\d+)')
after_regex = re.compile(r'After:\s+\[(\d+), (\d+), (\d+), (\d+)\]')


class Execution:
  """ An execution of an instruction """
  def __init__(self, instr, before, after):
    self.reg_before = before
    self.reg_after = after
    self.opcode = instr[0]
    self.A = instr[1]
    self.B = instr[2]
    self.C = instr[3]

  def __str__(self):
    return '{' + str(self.reg_before) + ' -> ' + str(self.opcode) + ' ' + str(self.A) + ' ' +  str(self.B) + ' ' +  str(self.C) + ' -> ' + str(self.reg_after) + '}'

  def __repr__(self):
    return self.__str__()


def parse_execution(lines):
  before_match = before_regex.match(lines[0])
  before_vals = [int(val) for val in before_match.groups()]

  instr_match = instr_regex.match(lines[1])
  instr_vals = [int(val) for val in instr_match.groups()]

  after_match = after_regex.match(lines[2])
  after_vals = [int(val) for val in after_match.groups()]    

  return Execution(instr_vals, before_vals, after_vals)


def read_input(path):
  executions = []
  with open(path) as infile:
    lines = []
    reading_exec = False
    for line in infile:
      if before_regex.match(line):
        reading_exec = True
        lines.append(line)
        continue
      if reading_exec:
        lines.append(line)
        if len(lines) == 3:
          reading_exec = False
          next_exec = parse_execution(lines)
          executions.append(next_exec)
          lines = []
          continue
  return executions


def find_candidate_functions(execution, funcs):
  possible_funcs = []
  for func in funcs	:
    result = func(execution.reg_before, execution.A, execution.B, execution.C)
    if result == execution.reg_after:
      possible_funcs.append(func)
  return possible_funcs


def run_program(program_file, opcode_func_map, registers):
  with open(program_file) as code:
    for instr in code:
      instr_match = instr_regex.match(instr)
      instr_vals = [int(val) for val in instr_match.groups()]      
      opcode = instr_vals[0]
      A = instr_vals[1]
      B = instr_vals[2]
      C = instr_vals[3]
      registers = opcode_func_map[opcode](registers, A, B, C)
  return registers


def main():
  infile = './input/executions.dat'
  executions = read_input(infile)
  print('Input', len(executions), 'executions from', infile)

  # part 1
  three_or_more_count = 0
  for ex in executions:
    possible_funcs = find_candidate_functions(ex, all_functions)
    possible_count = len(possible_funcs)
    if possible_count >= 3:
      three_or_more_count += 1

  print('found', three_or_more_count, 'executions with three or more possible opcodes')


  # part 2a -- find actual opcode mapping
  opcode_map = {}  
  funcs = all_functions[:]
  while len(opcode_map) < len(all_functions):
    print('number of funcs', len(funcs))
    for ex in executions:
      if ex.opcode in opcode_map.keys():
        continue
      possible_funcs = find_candidate_functions(ex, funcs)
      possible_count = len(possible_funcs)
      if possible_count == 1:
        opcode_map[ex.opcode] = possible_funcs[0]
        funcs.remove(possible_funcs[0])

  for ex in executions:
    if ex.opcode in opcode_map.keys():
      continue

  print('found definite opcode mappings for', len(opcode_map))

  program_file = './input/program.code'
  registers = [0, 0, 0, 0]
  result = run_program(program_file, opcode_map, registers)
  print(result)
 

# instruction definitions below here
# each should take an array of input register values and also the immediate values

def addr(before, A, B, C):
  """addr (add register) stores into register C the result of adding register A and register B."""
  after = before[:]
  after[C] = before[A] + before[B]
  return after


def addi(before, A, B, C):
  """addi (add immediate) stores into register C the result of adding register A and value B."""  
  after = before[:]
  after[C] = before[A] + B
  return after


def mulr(before, A, B, C):
  """mulr (multiply register) stores into register C the result of multiplying register A and register B."""
  after = before[:]
  after[C] = before[A] * before[B]
  return after


def muli(before, A, B, C):
  """muli (multiply immediate) stores into register C the result of multiplying register A and value B."""
  after = before[:]
  after[C] = before[A] * B
  return after


def banr(before, A, B, C):
  """banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
  after = before[:]
  after[C] = before[A] & before[B]
  return after


def bani(before, A, B, C):
  """bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
  after = before[:]
  after[C] = before[A] & B
  return after


def borr(before, A, B, C):
  """borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B."""
  after = before[:]
  after[C] = before[A] | before[B]
  return after


def bori(before, A, B, C):
  """bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
  after = before[:]
  after[C] = before[A] | B
  return after


def setr(before, A, B, C):
  """setr (set register) copies the contents of register A into register C. (Input B is ignored.)"""
  after = before[:]
  after[C] = before[A]
  return after


def seti(before, A, B, C):
  """seti (set immediate) stores value A into register C. (Input B is ignored.)"""
  after = before[:]
  after[C] = A
  return after


def gtir(before, A, B, C):
  """gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if A > before[B] else 0
  return after


def gtri(before, A, B, C):
  """gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if before[A] > B else 0
  return after


def gtrr(before, A, B, C):
  """gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if before[A] > before[B] else 0
  return after


def eqir(before, A, B, C):
  """eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if A == before[B] else 0
  return after


def eqri(before, A, B, C):
  """eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if before[A] == B else 0
  return after


def eqrr(before, A, B, C):
  """eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
  after = before[:]
  after[C] = 1 if before[A] == before[B] else 0
  return after

all_functions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


if __name__== "__main__":
  main()
