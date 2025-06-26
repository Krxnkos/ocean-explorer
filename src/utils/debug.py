import pygame

DEBUG_MODE = False
DEBUG_INTERVAL = 5000  # milliseconds between debug outputs
last_debug_time = 0

def debug_print(message, force=False):
    """Print debug messages only when DEBUG_MODE is on or force is True"""
    global last_debug_time
    current_time = pygame.time.get_ticks()
    
    # Always print forced messages or errors
    if force or "Error" in message:
        print(message)
        return
        
    # Only print regular debug messages when debug mode is on
    if DEBUG_MODE:
        # Further limit spammy position updates to the debug interval
        if "position" in message.lower() or "distance" in message.lower():
            if current_time - last_debug_time > DEBUG_INTERVAL:
                print(message)
                last_debug_time = current_time
        else:
            # Non-spammy messages can print more often
            print(message)