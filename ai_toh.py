import pygame
import platform
import uuid
from queue import PriorityQueue
import asyncio
import time

# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 1000, 800
PEG_COUNT = 5
DISK_COUNT = 5
PEG_WIDTH = 20
PEG_HEIGHT = 200
DISK_HEIGHT = 20
DISK_WIDTH_BASE = 60
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)


# Game setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi: 5 Pegs with AI Solver")
font = pygame.font.SysFont("arial", 24)
win_font = pygame.font.SysFont("arial", 48, bold=True)
clock = pygame.time.Clock()

# Game State
class GameState:
    def __init__(self):
        self.pegs = [list(range(DISK_COUNT, 0, -1))] + [[] for _ in range(PEG_COUNT - 1)]
        self.selected_peg = None
        self.move_count = 0
        self.ai_mode = False
        self.ai_moves = []
        self.ai_move_counter = 0
        self.ai_move_delay = 0
        self.ai_solution_found = False
        self.has_won = False

    def reset_game(self):
        self.pegs = [list(range(DISK_COUNT, 0, -1))] + [[] for _ in range(PEG_COUNT - 1)]
        self.selected_peg = None
        self.ai_mode = False
        self.move_count = 0
        self.ai_moves = []
        self.ai_move_counter = 0
        self.ai_move_delay = 0
        self.ai_solution_found = False
        self.has_won = False

    def check_win_condition(self):
        if len(self.pegs[-1]) == DISK_COUNT and all(len(peg) == 0 for peg in self.pegs[:-1]):
            self.has_won = True
            self.ai_mode = False # Stop AI mode on win
        return self.has_won

game_state = GameState()

# A* Search Algorithm Implementation
class State:
    def __init__(self, pegs, moves=0, parent=None, move=None):
        self.pegs = [peg[:] for peg in pegs]
        self.moves = moves
        self.parent = parent
        self.move = move
        self.id = str(uuid.uuid4())  # Unique ID for each state

    # Less than comparison for priority queue
    # This is used to prioritize states in the A* search algorithm
    def __lt__(self, other):
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())  
    
    def heuristic(self):
        # Heuristic: Number of disks not in the last peg
        return sum(len(peg) for peg in self.pegs[:-1])
    
    def is_goal(self):
        return len(self.pegs[-1]) == DISK_COUNT and all(len(peg) == 0 for peg in self.pegs[:-1])
    
    def get_neighbors(self):
        neighbors = []
        for i in range(PEG_COUNT):
            if self.pegs[i]:
                top_disk = self.pegs[i][-1]
                for j in range(PEG_COUNT):
                    if i != j:
                        if not self.pegs[j] or self.pegs[j][-1] > top_disk:
                            new_pegs = [peg[:] for peg in self.pegs]
                            new_pegs[i].pop()
                            new_pegs[j].append(top_disk)
                            neighbors.append(State(new_pegs, self.moves + 1, self, (i, j)))
        return neighbors
    
def a_star_search(initial_pegs):
    initial_state = State(initial_pegs)
    frontier = PriorityQueue()
    frontier.put((0, initial_state))
    explored = set()
    explored.add(str(initial_state.pegs))

    while not frontier.empty():
        _, current = frontier.get()
        if current.is_goal():
            moves = []
            while current.parent:
                moves.append(current.move)
                current = current.parent
            return moves[::-1]  # Return reversed moves to get the correct order
        for neighbor in current.get_neighbors():
            state_str = str(neighbor.pegs)
            if state_str not in explored:
                explored.add(state_str)
                priority = neighbor.moves + neighbor.heuristic()
                frontier.put((priority, neighbor))
    return []  # No solution found


# Drawing functions for the game
def draw_peg(x, y):
    pygame.draw.rect(screen, BLACK, (x - PEG_WIDTH // 2, y - PEG_HEIGHT, PEG_WIDTH, PEG_HEIGHT))

def draw_disk(x, y, size, color):
    width = DISK_WIDTH_BASE + size * 20
    pygame.draw.rect(screen, color, (x - width // 2, y - DISK_HEIGHT, width, DISK_HEIGHT))

def draw_button(text, x, y, width, height, color, text_color=BLACK):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def draw_game():
    screen.fill(WHITE)
    # Draw pegs 

    peg_spacing = WIDTH // (PEG_COUNT + 1)
    for i in range(PEG_COUNT):
        x = peg_spacing * (i + 1)
        y = HEIGHT - 50

        draw_peg(x, y)
        # Draw disks 
        for j, disk in enumerate(game_state.pegs[i]):
            color = [GREEN, BLUE, RED, YELLOW, PURPLE][(disk - 1) % 5]
            draw_disk(x, y - (j + 1) * DISK_HEIGHT, disk, color)

    # Draw UI elements
    move_text = font.render(f"Moves: {game_state.move_count}", True, BLACK)
    screen.blit(move_text, (10, 10))
    ai_btn_text = "Stop AI" if game_state.ai_mode else "Start AI"
    draw_button(ai_btn_text, WIDTH - 150, 10, 120, 40, GRAY)
    draw_button("Reset", WIDTH - 150, 60, 120, 40, RED)
    pygame.display.flip()

    # Draw win message
    if game_state.has_won:
        win_text = win_font.render("You Win!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    pygame.display.flip()


# Button click detection
def is_btn_clicked(x, y, btn_x, btn_y, width, height):
    return btn_x <= x <= btn_x + width and btn_y <= y <= btn_y + height

# Manual move validation check
def is_valid_move(from_peg, to_peg):
    if not game_state.pegs[from_peg]:
        return False
    if not game_state.pegs[to_peg]:
        return True
    return game_state.pegs[from_peg][-1] < game_state.pegs[to_peg][-1]

# Setup function for the game
def setup_game():
    game_state.reset_game()
    draw_game()


# update function for the game
def update_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_state.ai_mode:
            x, y = event.pos
            peg_spacing = WIDTH // (PEG_COUNT + 1)
            # Check peg selection
            for i in range(PEG_COUNT):
                peg_x = peg_spacing * (i + 1)
                if abs(x - peg_x) < PEG_WIDTH and HEIGHT - PEG_HEIGHT - 50 < y < HEIGHT:
                    if game_state.selected_peg is None:
                        if game_state.pegs[i]:
                            game_state.selected_peg = i
                    else:
                        if is_valid_move(game_state.selected_peg, i):
                            disk = game_state.pegs[game_state.selected_peg].pop()
                            game_state.pegs[i].append(disk)
                            game_state.move_count += 1
                            game_state.check_win_condition()
                            game_state.selected_peg = None
                        elif game_state.selected_peg == i:
                            game_state.selected_peg = None
            # Check button clicks
            if is_btn_clicked(x, y, WIDTH - 150, 10, 120, 40):
                game_state.ai_mode = not game_state.ai_mode
                if game_state.ai_mode and not game_state.ai_solution_found:
                    game_state.ai_moves = a_star_search(game_state.pegs)
                    game_state.ai_solution_found = True
                    game_state.ai_move_counter = 0
                    game_state.ai_move_delay = 0
            if is_btn_clicked(x, y, WIDTH - 150, 60, 120, 40):
                game_state.reset_game()
    return True


# main loop for non-Emscripten platforms
def main_local():
    setup_game()
    running = True
    while running:
        running = update_game()
        if game_state.ai_mode and game_state.ai_moves:
            game_state.ai_move_delay += 1
            if game_state.ai_move_delay >= FPS // 2:
                if game_state.ai_move_counter < len(game_state.ai_moves):
                    from_peg, to_peg = game_state.ai_moves[game_state.ai_move_counter]
                    disk = game_state.pegs[from_peg].pop()
                    game_state.pegs[to_peg].append(disk)
                    game_state.move_count += 1
                    game_state.check_win_condition()
                    game_state.ai_move_counter += 1
                    game_state.ai_move_delay = 0
                else:
                    game_state.ai_mode = False
        draw_game()
        clock.tick(FPS)
    pygame.quit()

# Run the game
if platform.system() == "Emscripten":
    async def main():
        setup_game()
        while running:
            running = update_game()
            if game_state.ai_mode and game_state.ai_moves:
                game_state.ai_move_delay += 1
                if game_state.ai_move_delay >= FPS // 2:
                    if game_state.ai_move_counter < len(game_state.ai_moves):
                        from_peg, to_peg = game_state.ai_moves[game_state.ai_move_counter]
                        disk = game_state.pegs[from_peg].pop()
                        game_state.pegs[to_peg].append(disk)
                        game_state.check_win_condition()
                        game_state.move_count += 1
                        game_state.ai_move_counter += 1
                        game_state.ai_move_delay = 0
                    else:
                        game_state.ai_mode = False
            draw_game()
            await asyncio.sleep(1.0 / FPS)
        pygame.quit()
    asyncio.ensure_future(main())
else:
    # If not running in Emscripten, run the local main loop
    main_local()


