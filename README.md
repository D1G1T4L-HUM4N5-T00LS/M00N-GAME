# 🐍 Cosmic Snake 🚀

A fun game that combines the classic Snake game with Space Invaders elements. Navigate your snake through space while collecting strawberries and avoiding (or shooting) cosmic invaders!

## Game Features

### Core Gameplay
- **Snake Movement**: Control your snake with arrow keys, collecting strawberries to grow longer
- **Space Invaders**: Alien invaders descend from the top of the screen, shooting bullets and trying to crash into you
- **Eat to Grow**: Each strawberry increases your score and makes your snake longer
- **Level Progression**: The game gets more challenging as you collect more strawberries
- **Wrapping Edges**: Snake can move through screen edges and appear on the opposite side

### Powerups
The game features three different powerups that randomly appear from the top of the screen:

1. **Speed Boost** (Blue): Temporarily increases your snake's movement speed
2. **Shield** (Cyan): Temporarily protects your snake head from collisions with invaders and bullets
3. **Bullet Power** (Orange): Temporarily allows your snake to shoot bullets and destroy invaders

### Scoring System
- **Strawberry**: +10 points
- **Powerup**: +15 points
- **Destroying an Invader** (with bullets): +20 points
- **Destroying an Invader** (with shield): +5 points
- **Level Up**: Every 50 points (5 strawberries)

### Game Controls
- **Arrow Keys**: Change snake direction
- **Space**: Shoot bullets (when bullet powerup is active)
- **P**: Pause/Unpause game
- **Q**: Quit (on game over screen)

## Installation and Running

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup
1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Game
```
python cosmic_snake.py
```

## Game Mechanics

### Snake Mechanics
- The snake continuously moves in the current direction
- It cannot reverse direction into itself (classic snake rule)
- Running into your own body ends the game unless you have a shield

### Invader Mechanics
- Invaders spawn randomly at the top of the screen
- They move downward at a steady pace
- Invaders can randomly shoot bullets downward
- If an invader reaches the bottom of the screen, it disappears
- If an invader hits your snake, you lose (unless shielded)

### Powerup Mechanics
- Powerups spawn from the top of the screen like invaders, but less frequently
- They last for a limited time once collected
- Active powerups are displayed at the top of the screen
- Multiple powerups can be active simultaneously

## Customization

You can modify the game by editing the constants at the top of `cosmic_snake.py`:

- Change game dimensions/grid size
- Adjust snake/invader speeds
- Modify spawn rates
- Add custom images by modifying the `load_image` function

## Game Development Notes

This game uses placeholder colored rectangles for game objects. You can enhance the visual experience by adding real images for:
- Snake head and body
- Strawberries
- Invaders
- Bullets
- Powerups

## Credits

Developed as a Python game demonstration combining the classic Snake game with Space Invaders elements.

## License

This project is open source and available for anyone to use and modify. 