from math import ceil, sqrt
import re

ip_regex = re.compile(r'#ip (\d+)')
instruction_regex = re.compile(r'(\w{4}) (\d+) (\d+) (\d+)')

def read_input(path):
  ip_reg = 0
  code = []
  with open(path) as infile:
    i = 0
    for line in infile:
      if i == 0:
        match = ip_regex.match(line)
        ip_reg = int(match.groups()[0])
        i += 1
      else:
        match = instruction_regex.match(line)
        func = func_map[match.groups()[0]]
        A = int(match.groups()[1])
        B = int(match.groups()[2])
        C = int(match.groups()[3])
        code.append((func, A, B, C))  
  return ip_reg, code


def run_code(regs, init_ip, ip_reg, code, print_after=1000000):
  ip = init_ip
  cnt = 0
  while True:
    if ip >= len(code):
      break
    inst = code[ip]
    A = inst[1]
    B = inst[2]
    C = inst[3]
    regs[ip_reg] = ip
    regs_before = regs[:]
    regs = inst[0](regs, A, B, C)
    if cnt >= print_after:
      print("{}: ip={} {} {} {} {} {} {}".format(cnt, ip, regs_before, inst[0].__name__, A, B, C, regs))
    ip = regs[ip_reg]
    ip += 1
    cnt += 1
  return regs


def main():
  path = './input/input.dat'
  ip_reg, code = read_input(path)

  i = 0
  for inst in code:
    print("{} {}".format(i, inst[0].__name__))
    i += 1
  #return

  regs = [0, 0, 0, 0, 0, 0]
  #regs = run_code(regs, 0, ip_reg, code)
  #print('part 1:', regs[0])
  
  regs = [1, 0, 0, 0, 0, 0]
  #regs = run_code(regs, 0, ip_reg, code)

  # on manual inspection, found that the program will loop until register 1 == register 2 = 10551354
  # register 1 is incrementing slowly. here is an output example:
  # [0, 0, 10551354, 4, 1, 1266937]
  # so try running this by setting the reg[5] value to almost reg[2], and incrementing ip

  #regs = [0, 0, 10551354, 7, 1, 10551344]
  #regs = run_code(regs, 8, ip_reg, code, 0)

  # now we have moved past where reg[0] = 0, and now reg[0] = 1, but 
  # the relationship between reg[5] and reg[1] is reg[1] = 2*reg[5]
  # try [1, 0, 10551354, 7, 2, 5]
  # but set reg[5] to be almost half of 10551354

  
  #regs = [1, 0, 10551354, 7, 2, 5275674]
  #regs = run_code(regs, 8, ip_reg, code, 0)
  

  # ok, reg[0] = 3 and NOW we have reg[1]>reg[2] all the time!
  # so that eqrr is not the instr that will change things this time
  # but a gtrr 5 2 1 is! when reg[5] > reg[2], reg[1] will be set to 1 instead of the 0!
  # so lets skip ahead to [3, 0, 10551354, 7, 2, 10551352]

  #regs = [3, 0, 10551354, 7, 2, 10551352]
  #regs = run_code(regs, 8, ip_reg, code, 0)

  # now reg[0] still = 3, but reg[4] = 3 (which seems to be how much we are counting by)
  # and also not reg[1] is small again, and reg[1] = 3*reg[5], so lets do:
  # [3, 0, 10551354, 7, 3, 10551354/3 - 1] = 3517117

  #regs = [3, 0, 10551354, 7, 3, 3517116]
  #regs = run_code(regs, 8, ip_reg, code, 0)


  # do we have a pattern yet?
  # of the 5 sections I've looked at so far, where N = 10551354
  # reg[0] reg[1]           reg[4]    reg[5]
  #   0     <N, counts by 1   1         counts up from 0 to N
  #   1     <N, counts by 2   2         counts up from 0 to N/2
  #   3     >N, counts by 2   2         counts up from N/2 until >N
  #   3     <N, counts by 3   3         counts up from 0 to N/3
  #   6     >N, counts by 3   3         counts up from N/3 to N??? (test this)
  #   6     <N, counts by 4   4         counts up from 0 to N/4??? (test this) (no!)

  #regs = [6, 0, 10551354, 7, 3, 10551352]     
  #regs = run_code(regs, 8, ip_reg, code, 0)

  # ok, try this for counting up to N/4...

  #regs = [6, 0, 10551354, 7, 4, 2637836]     
  #regs = run_code(regs, 8, ip_reg, code, 0)
  
  # no! that went right past because reg[1] skipped over 10551354! Then will it go up until 
  # r[5]>r[2]?
  # try this...
  
  #regs = [6, 0, 10551354, 7, 4, 10551352]     
  #regs = run_code(regs, 8, ip_reg, code, 0)
  
  # ok yup, that reset r[5], but did not increment r[0]!
  # so! here is what seems to be happening!
  # -- start with factor of f=1, sum = 0
  # -- increment a value (x), starting from zero, by f, (x += f)
  # -- also increment counter c by c+=1
  # -- if at any point x==N, then add f to sum
  # -- else, once counter c>N, increment f <- f+1
  # so we are adding up factors of N!
  # 
  # try to add up factors of N
  
  N = 10551354
  factors = [i for i in range(1, N+1) if not N%i]
  print(sum(factors))
  

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


func_map = {'addr': addr, 'addi': addi, 'mulr': mulr, 'muli': muli, 'banr': banr, 'bani': bani, 'borr': borr, 'bori': bori, 'setr': setr, 'seti': seti, 'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr, 'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr}


if __name__== "__main__":
  main()
