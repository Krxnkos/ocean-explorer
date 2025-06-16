# Setup Instructions for Ocean Explorer

This document will guide you through installing and running the Ocean Explorer game.

## Requirements

- Python 3.6 or higher
- Pygame module
- Basic computer with audio capabilities

## Installation Steps

### 1. Install Python

If you don't have Python installed:

1. Visit [python.org](https://www.python.org/downloads/)
2. Download the latest version for your operating system
3. Run the installer
4. **Important:** Check the box "Add Python to PATH" during installation
5. Complete the installation

### 2. Install Pygame and Dependencies

Open your command prompt or terminal:

**Option 1: Using pip directly**
```
pip install pygame
```

**Option 2: Using the requirements file**
Navigate to the ocean-explorer directory and run:
```
pip install -r requirements.txt
```

### 3. Download Game Assets

For the game to run properly, you'll need to create an assets folder structure and add appropriate images and sounds:

1. In the ocean-explorer folder, create these directories:
   - `assets/images`
   - `assets/sounds`

2. You'll need the following image files in the `assets/images` folder:
   - player.png (a submarine or diver)
   - dolphin.png
   - turtle.png
   - starfish.png
   - octopus.png
   - red_fish.png
   - ocean_bg.png (ocean background)

3. You'll need the following sound files in the `assets/sounds` folder:
   - correct.wav (sound for correct answers)
   - wrong.wav (sound for incorrect answers)
   - ocean_music.wav (background music)

You can find free assets on sites like:
- [OpenGameArt.org](https://opengameart.org/)
- [Freesound.org](https://freesound.org/)
- [Kenney.nl](https://kenney.nl/assets)

### 4. Running the Game

1. Open a command prompt or terminal
2. Navigate to the ocean-explorer directory
3. Run the game with:
```
python game.py
```

## Troubleshooting

### Common Issues:

**"ModuleNotFoundError: No module named 'pygame'"**
- Run `pip install pygame` to install the pygame module

**"FileNotFoundError" for images or sounds**
- Make sure you've created the assets folder structure correctly
- Check that all required asset files are in the correct folders
- Verify file names match exactly what's used in the code

**Game runs slowly or with lag**
- Reduce the window size in the code (SCREEN_WIDTH and SCREEN_HEIGHT)
- Close other applications running on your computer

## Controls

- Use the arrow keys to move the player
- Click answer buttons with your mouse
- Exit the game by closing the window

## Need Help?

If you encounter any issues, please:
1. Verify you have all the required assets
2. Check that Python and Pygame are installed correctly
3. Make sure you're running the game from the correct directory

Enjoy exploring the ocean!
