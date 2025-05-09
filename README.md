# Tower of Hanoi AI Game (5 Pegs)

This is an interactive Tower of Hanoi game implemented in Python using Pygame. The game supports 5 pegs (configurable) and includes an AI solver that uses the A* search algorithm to find the optimal solution. Players can either solve the puzzle manually or let the AI solve it automatically.

## Prerequisites

To run the game, you need Python 3.6 or higher installed on your system. The game relies on the `pygame` library for rendering and user interaction.

## Installation

1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - Ensure Python is added to your system's PATH during installation.

    - Clone or download the repository containing the game files (ai_toh.py, README.md, LICENSE).
    - git clone (repo_link)
    - Ensure all files are in the same directory.

2. **Install Pygame**:
   - Open a terminal or command prompt and run the following command to install Pygame:
     pip install pygame

3. **Running the Game**
    - Execute the Python script using the following command:
    - python ai_toh.py

# How to Play
- Manual Mode:
- Click on a peg to select it (if it has disks).
- Click another peg to move the top disk from the selected peg to the destination peg (if the move is valid).
- The goal is to move all disks to the last peg, following the standard Tower of Hanoi rules:
- Only one disk can be moved at a time.
- A larger disk cannot be placed on top of a smaller disk.

# AI Mode:
- Click the "Start AI" button to let the A* search algorithm solve the puzzle automatically.
- The AI will compute the optimal sequence of moves.
- The AI uses the A* search algorithm with a heuristic to find the shortest path to the solution.

# Reset:
    - Click the "Reset" button to restart the game with the initial configuration.

    Win Condition:
    - The game is won when all disks are moved to the last peg. A "You Win!" message will appear.

    Configuration (Optional)
    - You can modify the following constants in ai_toh.py to customize the game:
    - PEG_COUNT: Number of pegs (default: 5).
    - DISK_COUNT: Number of disks (default: 5).
    - Adjust these values to experiment with different puzzle configurations.