def score_new_recipes(scores, current_recipes):
  val = 0
  for recipe in current_recipes:
    val += int(scores[recipe])
  for c in str(val):
    scores.append(c)
  return scores

def pick_new_recipe(scores, current_recipe):
  step = int(scores[current_recipe]) + 1
  return (current_recipe + step)%len(scores)

def main():
  current_recipes = [0, 1]
  scores = ['3', '7']
  score_string = "".join(scores)

  index = 50
  substring = '503761'
  cnt = 0  
#  for i in range(index+20):
  while True:
    if len(scores) > 6 and substring in "".join(scores[-(len(substring)+1):]):
      break
    cnt += 1
    if cnt%1000000 == 0:
      print(cnt)
    scores = score_new_recipes(scores, current_recipes)
    for elf in range(len(current_recipes)):
      current_recipes[elf] = pick_new_recipe(scores, current_recipes[elf])
  
  score_string = "".join(scores)
  print(score_string.index(substring))

if __name__== "__main__":
  main()
