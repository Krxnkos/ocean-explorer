# Ocean Explorer Debug Controls

If you're having trouble with the game progression, these special debug controls can help:

## How to Use Debug Features

The game now has debugging features that can be toggled on and off:
- Press **D** to toggle debug mode (shows additional information)
- Press **C** to toggle collision circles around creatures
- Debug status is shown in the top-right corner of the screen

## Controlling Console Output

By default, debug output to the terminal is minimized to prevent flooding:

- When debug mode is OFF, only critical messages are shown
- When debug mode is ON, more information is shown but frequency is limited
- Edit `debug_config.py` to customize debug behavior

## Special Debug Keys

Press these keys for special debug functions:

- **D Key**: Toggle debug mode on/off
- **C Key**: Toggle collision circle visibility
- **R Key**: Reset game state and start over
- **F Key**: Force transition to the next state 
- **1-5 Keys**: Teleport to specific creatures
- **S Key**: Add a star to your collection
- **G Key**: Go directly to game over screen

## Understanding the Debug Information

At the bottom of the screen, you'll see:
- Current state: EXPLORE, QUIZ, REWARD, or GAME_OVER
- Stars collected / Total stars

For more detailed information, press **D** to enable debug mode, then check the console.

## Advanced Configuration

For developers who need to customize the debugging experience:

1. Open `debug_config.py` to modify debugging settings
2. You can change:
   - Debug mode on startup
   - Debug output level
   - Position update frequency
   - Whether to log to file instead of console

## Diagnosing Common Issues

### If the game seems stuck:
1. Check the current state at the bottom of the screen
2. Press D to enable debug mode
3. Press F to force the game to the next state
4. Try teleporting to creatures with number keys (1-5)

### If creatures don't disappear after answering:
- This is expected behavior - visited creatures remain visible but won't trigger questions again
- Check your star count to see if you got credit for the answer

### If you can't reach all creatures:
- Press the number keys (1-5) to teleport directly to each creature
- Press C to see collision circles that show interaction areas

## Reporting Issues

If you continue to have problems, please report:
1. What steps you took before the issue occurred
2. The current state shown at the bottom of the screen
3. How many stars you had collected
4. Any error messages shown in the console
5. Which creature you were trying to interact with
