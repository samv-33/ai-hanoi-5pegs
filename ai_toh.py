import pygame
import platform
import uuid
from queue import PriorityQueue
import asyncio

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


# Game setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi: 5 Pegs with AI Solver")
font = pygame.font.SysFont("Lexend", 24)

# Game State
class GameState:
    def __init__(self):
        self.pegs = [list(range(DISK_COUNT, 0, -1))] + [[] for _ in range(PEG_COUNT - 1)]
        self.selected_peg = None
        self.move_count = 0
        self.ai_moves = []
        self.ai_move_counter = 0
        self.ai_move_delay = 0
        self.ai_solution_found = False

    def reset_game(self):
        self.pegs = [list(range(DISK_COUNT, 0, -1))] + [[] for _ in range(PEG_COUNT - 1)]
        self.selected_peg = None
        self.move_count = 0
        self.ai_moves = []
        self.ai_move_counter = 0
        self.ai_move_delay = 0
        self.ai_solution_found = False

game_state = GameState()

# A* Search Algorithm Implementation
class State:
    def __init__(self, pegs, moves=0, parent=None, move=None):
        self.pegs = [peg[:] for peg in pegs]
        self.moves = moves
        self.parent = parent
        self.move = move
        self.id = str(uuid.uuid4())  # Unique ID for each state













        


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
            color = [GREEN, BLUE, RED, YELLOW, PURPLE][disk - 1]
            draw_disk(x, y - (j + 1) * DISK_HEIGHT, disk, color)

