import random
from rustyvale.background import Level
terrain = {" ":20,"-":1, "~":10, "h":1}

edges = "[","]"

def random_level(size):
   level = ''
   old_line = "[" + size * " " + "]"
   old_x = " "
   lines = []
   for y in range(size):
      line = '['
      for x in range(size):
         updated_terrain = dict(terrain)
         updated_terrain[old_x] += 100
         choice_str = ''.join([t * updated_terrain[t] for t in updated_terrain ])
         pixel = random.choice(choice_str)
         line += pixel
         old_x = pixel
      
      line += "]\n"
      lines.append(line)
      old_line = line
      print line,
   return  ''.join(lines)

if __name__ == "__main__":
   my_l = Level('random level',random_level(10), verbose=False)
   my_l.loop()
