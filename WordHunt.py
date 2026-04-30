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
font = pygame.font.Font("dogicapixelbold.ttf", 25)

rows, cols = 4, 4
cell_size = 100
gap = 15
found_words = set()

WHITE = (255,255,255)
LIGHT = (170,170,170)
DARK = (100,100,100)
BG = (78, 159, 229)

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

def get_score(word):
   length = len(word)
   if length < 3: return 0
   if length <= 4: return 100
   if length == 5: return 200
   if length == 6: return 300
   if length == 7: return 500
   return 800

def game():
  global mouse_down, selected_path, current_word, score, color
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

        if len(word) >= 3 and word in dictionary and word not in found_words:
            found_words.add(word)
            score += get_score(word)
            current_word = word + " ✓"
        
        selected_path = []
            
      screen.fill(BG)
      text = font.render("Word: " + current_word, True, color)
      screen.blit(text, (100, 100))
      
      sidebar_x = WIDTH - 1050
      y_offset = 200

      for w in sorted(found_words):
        word_surface = font.render(w, True, (0, 0, 0))
        screen.blit(word_surface, (sidebar_x + 20, y_offset))
        y_offset += 30


      score_text = font.render("Score: " + str(score), True, (0, 0, 0))
      screen.blit(score_text, (800, 100))

      if mouse_down:
        cell = get_cell(pygame.mouse.get_pos())
        if cell and cell not in selected_path:
            selected_path.append(cell)
        
      word = "".join(grid[r][c].letter for (r, c) in selected_path).lower()

      if word in dictionary and len(word) >= 3:
        current_word = word
        color = (0, 150, 0)
      else:
        current_word = word
        color = (150, 0, 0)

      for (r, c) in selected_path:
        x = start_x + c * (cell_size + gap)
        y = start_y + r * (cell_size + gap)
        
        highlight_letter = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

        if word in dictionary and len(word) >= 3:
          pygame.draw.rect(highlight_letter, (0, 255, 0, 120), (0, 0, cell_size, cell_size), border_radius=15)
        else:
          pygame.draw.rect(highlight_letter, (255, 0, 0, 120), (0, 0, cell_size, cell_size), border_radius=15)

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

def start_menu():
   while True:
    screen.fill(BG)
    mouse = pygame.mouse.get_pos()

    play_button = pygame.Rect((WIDTH - 140)//2, 300, 140, 50)
    quit_button = pygame.Rect((WIDTH - 140)//2, 380, 140, 50)

    pygame.draw.rect(screen, LIGHT if play_button.collidepoint(mouse) else DARK, play_button)
    pygame.draw.rect(screen, LIGHT if quit_button.collidepoint(mouse) else DARK, quit_button)

    title = font.render("WORD HUNTING", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH//2, 100))
    play_text = font.render("Play", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    
    screen.blit(title, title_rect)
    screen.blit(play_text, play_text.get_rect(center=play_button.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        if play_button.collidepoint(mouse):
          game()
        
        if quit_button.collidepoint(mouse):
          pygame.quit()
          sys.exit()
      
    pygame.display.update()

start_menu()
        
