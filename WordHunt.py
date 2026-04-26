import pygame
import sys
import random

with open("words.txt") as f:
   dictionary = set(word.strip().lower() for word in f)

pygame.init()

#screen setup
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Word Hunt")
font = pygame.font.SysFont(None, 40)

rows, cols = 4, 4
cell_size = 100

grid_width = cols * cell_size
grid_height = rows * cell_size

start_x = (WIDTH - grid_width) // 2
start_y = (HEIGHT - grid_height) // 2

current_word = ""
color = (0, 0, 0)

class Cell:
    def __init__(self, letter):
      self.letter = letter


letters = list("TREVMADETHISGAME")
grid = []
index = 0

for row in range(rows):
  row_list = []
  for col in range(cols):
    row_list.append(Cell(letters[index]))
    index += 1
  grid.append(row_list)

selected_path = []
mouse_down = False

def get_cell(pos):
   mx, my = pos
   col = (mx - start_x) // cell_size
   row = (my - start_y) // cell_size

   if 0 <= row < rows and 0 <= col < cols:
      return (row, col)
   return None

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_down = True
      selected_path = []

    if event.type == pygame.MOUSEBUTTONUP:
       mouse_down = False
       word = "".join(grid[r][c].letter for (r, c) in selected_path).lower()

       if word in dictionary:
          current_word = word + " - valid!"
          color = (0, 150, 0)
       else:
          current_word = word + " - invalid!"
          color = (150, 0, 0)
          
    screen.fill((255, 255, 255))
    text = font.render("Word: " + current_word, True, color)
    screen.blit(text, (100, 100))

    if mouse_down:
       cell = get_cell(pygame.mouse.get_pos())
       if cell and cell not in selected_path:
          selected_path.append(cell)

    for (r, c) in selected_path:
      x = start_x + c * cell_size
      y = start_y + r * cell_size
       
      highlight_letter = pygame.Surface((cell_size, cell_size))
      highlight_letter.set_alpha(120)
      highlight_letter.fill((0, 150, 255))
      screen.blit(highlight_letter, (x, y))

      for i in range(len(selected_path) - 1):
        r1, c1 = selected_path[i]
        r2, c2 = selected_path[i + 1]

        x1 = start_x + c1 * cell_size + cell_size // 2
        y1 = start_y + r1 * cell_size + cell_size // 2

        x2 = start_x + c2 * cell_size + cell_size // 2
        y2 = start_y + r2 * cell_size + cell_size // 2
      
        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), 5)
       
    for row in range(rows):
        for col in range(cols):
            
            x = start_x + col * cell_size
            y = start_y + row * cell_size

            pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 2)

            letter = grid[row][col].letter

            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(x + cell_size // 2, y + cell_size // 2)
            )

            screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)
