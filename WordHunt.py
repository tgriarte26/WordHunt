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
gap = 15


grid_width = cols * cell_size + (cols - 1) * gap
grid_height = rows * cell_size + (rows - 1) * gap

start_x = (WIDTH - grid_width) // 2
start_y = (HEIGHT - grid_height) // 2

current_word = ""
color = (0, 0, 0)
score = 0

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

   for row in range(rows):
      for col in range(cols):
         x = start_x + col * (cell_size + gap)
         y = start_y + row * (cell_size + gap)

         rect = pygame.Rect(x, y, cell_size, cell_size)
         if rect.collidepoint(mx, my):
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

       if word in dictionary and len(word) >= 3:
          current_word = word + " - valid!"
          color = (0, 150, 0)
          score += 50 * len(word)
       else:
          current_word = word + " - invalid!"
          color = (150, 0, 0)
          
    screen.fill((255, 255, 255))
    text = font.render("Word: " + current_word, True, color)
    screen.blit(text, (100, 100))

    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (800, 100))

    if mouse_down:
       cell = get_cell(pygame.mouse.get_pos())
       if cell and cell not in selected_path:
          selected_path.append(cell)

    for (r, c) in selected_path:
      x = start_x + c * (cell_size + gap)
      y = start_y + r * (cell_size + gap)
       
      highlight_letter = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
      pygame.draw.rect(highlight_letter, (0, 150, 255, 120), (0, 0, cell_size, cell_size), border_radius=15)

      screen.blit(highlight_letter, (x, y))

      for i in range(len(selected_path) - 1):
        r1, c1 = selected_path[i]
        r2, c2 = selected_path[i + 1]

        x1 = start_x + c1 * (cell_size + gap) + cell_size // 2
        y1 = start_y + r1 * (cell_size + gap)+ cell_size // 2

        x2 = start_x + c2 * (cell_size + gap) + cell_size // 2
        y2 = start_y + r2 * (cell_size + gap) + cell_size // 2
      
        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), 5)
       
    for row in range(rows):
        for col in range(cols):
            
            x = start_x + col * (cell_size + gap)
            y = start_y + row * (cell_size + gap)

            pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 2, border_radius=10)

            letter = grid[row][col].letter

            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(x + cell_size // 2, y + cell_size // 2)
            )

            screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)
