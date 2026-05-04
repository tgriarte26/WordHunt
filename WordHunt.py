import pygame
import sys
import random
import string

dictionary = {
  "tree", "train", "brain", "game", "code",
  "python", "learn", "stack", "logic", "pixel",
  "random", "board", "letter", "score", "hunt"
}
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

GAME_TIME = 60
start_ticks = None
time_left = GAME_TIME
game_over = False

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
random.shuffle(letters)

index = 0

prefixes = set()
for word in dictionary:
  for i in range(1, len(word)):
    prefixes.add(word[:i])
    
def get_neighbors(r, c):
  directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

  neighbors = []
  for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
      neighbors.append((nr, nc))
  return neighbors

def dfs(r, c, visited, current_word, found, grid):
  current_word += grid[r][c].letter.lower()
  
  # Limit word length to prevent excessive exploration
  if len(current_word) > 8:
    return
    
  if current_word not in prefixes and current_word not in dictionary:
    return
  
  if len(current_word) >= 3 and current_word in dictionary:
    found.add(current_word)

  visited.add((r, c))

  for nr, nc in get_neighbors(r, c):
    if(nr, nc) not in visited:
      dfs(nr, nc, visited, current_word, found, grid)
      
  visited.remove((r, c))

def find_all_words(grid=None):
  if grid is None:
    grid = globals()['grid']
  found = set()

  for r in range(rows):
    for c in range(cols):
      dfs(r, c, set(), "", found, grid)
  
  return found

def get_random_words(dictionary, count=5):
  valid_words = [w for w in dictionary if 3 <= len(w) <= 6]
  return random.sample(valid_words, count)



def place_word(grid, word):
  for _ in range(100):
    path = []
    used = set()
    
    r = random.randint(0, rows-1)
    c = random.randint(0, cols-1)

    path.append((r, c))
    used.add((r, c))

    for i in range(1, len(word)):
      neighbors = [n for n in get_neighbors(r, c) if n not in used]
      if not neighbors:
        break
      
      r, c = random.choice(neighbors)
      path.append((r, c))
      used.add((r, c))

    if len(path) == len(word):
      for (r, c), letter in zip(path, word):
        grid[r][c].letter = letter.upper()
      return True
  return False
  
def generate_board():
  # Create a board by placing a few words and filling the rest with random letters
  grid = [[Cell("") for _ in range(cols)] for _ in range(rows)]
  
  # Try to place 3-4 words
  words_to_place = get_random_words(dictionary, count=4)
  placed_count = 0
  
  for word in words_to_place:
    if place_word(grid, word):
      placed_count += 1
    if placed_count >= 3:  # Stop after placing 3 words
      break

  # Fill remaining cells with random letters
  letter_pool = "EEEEEEEEEEEEAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTT"
  
  for r in range(rows):
    for c in range(cols):
      if grid[r][c].letter == "":
        grid[r][c].letter = random.choice(letter_pool)

  # Check how many words we have
  possible_words = find_all_words(grid)
  print(f"Generated board with {len(possible_words)} possible words (placed {placed_count} words)")
  
  return grid

grid = generate_board()

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

def analyze_board(found_words):
  all_words = find_all_words()
  longest_word = max(all_words, key=len) if all_words else ""
  total_possible_score = sum(get_score(w) for w in all_words)
  missed_words = all_words - found_words

  return longest_word, total_possible_score, missed_words

def end_screen(final_score, found_words, all_words):
  while True:
    screen.fill(BG)
    mouse = pygame.mouse.get_pos()

    title_font = pygame.font.Font("dogicapixelbold.ttf", 40)
    title = title_font.render("GAME OVER", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    score_text = font.render(f"Final Score: {final_score}", True, (0, 0, 0))
    screen.blit(score_text, (100, 150))
    
    found_count = font.render(f"Words Found: {len(found_words)}", True, (0, 0, 0))
    screen.blit(found_count, (100, 200))
    
    total_count = font.render(f"Total Possible: {len(all_words)}", True, (0, 0, 0))
    screen.blit(total_count, (100, 250))
    
    y_offset = 320
    words_label = font.render("Words Found:", True, (0, 0, 0))
    screen.blit(words_label, (100, y_offset))
    y_offset += 40
    
    for word in sorted(found_words):
      word_text = font.render(word, True, (0, 150, 0))
      screen.blit(word_text, (120, y_offset))
      y_offset += 30
      if y_offset > HEIGHT - 300:
        break
    
    # Show possible words
    y_offset += 20
    possible_label = font.render("Possible Words:", True, (0, 0, 0))
    screen.blit(possible_label, (100, y_offset))
    y_offset += 40
    
    for word in sorted(all_words):
      color = (0, 150, 0) if word in found_words else (150, 0, 0)
      word_text = font.render(word, True, color)
      screen.blit(word_text, (120, y_offset))
      y_offset += 30
      if y_offset > HEIGHT - 150:
        break
    
    menu_button = pygame.Rect((WIDTH - 200)//2, HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, LIGHT if menu_button.collidepoint(mouse) else DARK, menu_button)
    menu_text = font.render("Return to Menu", True, (255, 255, 255))
    screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        if menu_button.collidepoint(mouse):
          return

    pygame.display.update()
    clock.tick(60)

def game():
  global mouse_down, selected_path, current_word, score, color, start_ticks, time_left, game_over, found_words, grid

  found_words = set()
  score = 0
  current_word = ""
  color = (0, 0, 0)
  grid = generate_board()
  selected_path = []
  
  start_ticks = pygame.time.get_ticks()
  game_over = False

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
    timer_text = font.render("Time: " + str(time_left), True, (0, 0, 0))
    screen.blit(timer_text, (100, 50))

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
      y1 = start_y + r1 * (cell_size + gap) + cell_size // 2

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

    if not game_over:
      seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
      time_left = max(0, GAME_TIME - int(seconds_passed))

      if time_left == 0:
        game_over = True
        all_words = find_all_words()
        end_screen(score, found_words, all_words)
        return
      
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
