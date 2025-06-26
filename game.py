import os
import pygame
from src.core.game import Game
from src.utils.debug import debug_print

def main():
    # Create asset directories if they don't exist
    os.makedirs(os.path.join('assets', 'images'), exist_ok=True)
    os.makedirs(os.path.join('assets', 'sounds'), exist_ok=True)
    
    debug_print("Ocean Explorer starting...", True)
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

