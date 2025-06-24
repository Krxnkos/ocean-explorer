"""
Debug configuration for Ocean Explorer game.
This file lets you configure debugging options without modifying the main game code.
"""

# Set to True to enable debug mode on startup, False for normal mode
DEBUG_ON_STARTUP = False

# Show collision circles by default
SHOW_COLLISION_CIRCLES = False

# Debug output control
# 0 = Minimal (errors and important events only)
# 1 = Normal (state changes and interactions)
# 2 = Verbose (includes positions and collisions)
# 3 = Very verbose (includes all updates)
DEBUG_LEVEL = 1

# Time between position updates in milliseconds
POSITION_UPDATE_INTERVAL = 1000

# Write debug info to a log file instead of console
LOG_TO_FILE = False
LOG_FILENAME = "ocean_explorer_debug.log"

"""
Keyboard Shortcuts Reference:

D - Toggle debug mode on/off
C - Toggle collision circles
R - Reset/restart the game
F - Force next game state
1-5 - Teleport to creatures
S - Add a star
G - Go to game over screen
"""
