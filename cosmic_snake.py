import pygame
import random
import sys
import os
import time
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Base speed
INVADER_SPEED = 1.5
INVADER_SPAWN_RATE = 0.02  # Probability of spawning an invader per frame
MAX_INVADERS = 10
INVADER_FIRE_RATE = 0.005  # Probability of an invader firing per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cosmic Snake")
clock = pygame.time.Clock()

# Load images (we'll use placeholder rectangles for now, but you can add real images)
def load_image(name, size=(GRID_SIZE, GRID_SIZE)):
    try:
        image = pygame.Surface(size)
        if name == "snake_head":
            image.fill(GREEN)
        elif name == "snake_body":
            image.fill((0, 200, 0))
        elif name == "strawberry":
            image.fill(RED)
        elif name == "invader":
            image.fill(PURPLE)
        elif name == "bullet":
            image.fill(YELLOW)
        elif name == "speed_powerup":
            image.fill(BLUE)
        elif name == "shield_powerup":
            image.fill((0, 255, 255))
        elif name == "bullet_powerup":
            image.fill((255, 165, 0))
        return image
    except pygame.error as e:
        print(f"Couldn't load image: {e}")
        return pygame.Surface(size)

# Direction enum
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# PowerUp types
class PowerUpType(Enum):
    SPEED = 0
    SHIELD = 1
    BULLET = 2

# Game object classes
class Snake:
    def __init__(self):
        self.reset()
        self.head_image = load_image("snake_head")
        self.body_image = load_image("snake_body")
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.growing = False
        self.speed_boost = 0
        self.shield_active = False
        self.shield_timer = 0
        self.can_shoot = False
        self.bullet_timer = 0
        self.last_shot_time = 0
        self.shot_cooldown = 500  # milliseconds
        
    def get_head_position(self):
        return self.positions[0]
    
    def change_direction(self, direction):
        if len(self.positions) > 1:
            # Prevent the snake from reversing
            if ((direction == Direction.UP and self.direction != Direction.DOWN) or 
                (direction == Direction.DOWN and self.direction != Direction.UP) or 
                (direction == Direction.LEFT and self.direction != Direction.RIGHT) or 
                (direction == Direction.RIGHT and self.direction != Direction.LEFT)):
                self.next_direction = direction
        else:
            self.next_direction = direction
    
    def move(self):
        head = self.get_head_position()
        dx, dy = self.next_direction.value
        new_x = (head[0] + dx) % GRID_WIDTH
        new_y = (head[1] + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Check for collision with self
        if new_head in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_head)
        self.direction = self.next_direction
        
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False
            self.length += 1
            
        return True
    
    def grow(self):
        self.growing = True
    
    def activate_speed_boost(self, duration=5):
        self.speed_boost = duration * SNAKE_SPEED
    
    def activate_shield(self, duration=5):
        self.shield_active = True
        self.shield_timer = duration * SNAKE_SPEED
    
    def activate_bullet_powerup(self, duration=10):
        self.can_shoot = True
        self.bullet_timer = duration * SNAKE_SPEED
    
    def update_powerups(self):
        if self.speed_boost > 0:
            self.speed_boost -= 1
            
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.can_shoot:
            self.bullet_timer -= 1
            if self.bullet_timer <= 0:
                self.can_shoot = False
    
    def shoot(self):
        if not self.can_shoot:
            return None
            
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shot_cooldown:
            return None
            
        self.last_shot_time = current_time
        head = self.get_head_position()
        # Adjust bullet position to be centered at the head
        bullet_pos = (head[0] * GRID_SIZE + GRID_SIZE // 2, head[1] * GRID_SIZE)
        return Bullet(bullet_pos, -1)  # -1 for upward direction
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            
            if i == 0:  # Head
                surface.blit(self.head_image, rect)
                # Draw eyes on the head
                if self.direction == Direction.UP:
                    pygame.draw.circle(surface, BLACK, (rect.x + GRID_SIZE // 3, rect.y + GRID_SIZE // 3), 2)
                    pygame.draw.circle(surface, BLACK, (rect.x + 2 * GRID_SIZE // 3, rect.y + GRID_SIZE // 3), 2)
                elif self.direction == Direction.DOWN:
                    pygame.draw.circle(surface, BLACK, (rect.x + GRID_SIZE // 3, rect.y + 2 * GRID_SIZE // 3), 2)
                    pygame.draw.circle(surface, BLACK, (rect.x + 2 * GRID_SIZE // 3, rect.y + 2 * GRID_SIZE // 3), 2)
                elif self.direction == Direction.LEFT:
                    pygame.draw.circle(surface, BLACK, (rect.x + GRID_SIZE // 3, rect.y + GRID_SIZE // 3), 2)
                    pygame.draw.circle(surface, BLACK, (rect.x + GRID_SIZE // 3, rect.y + 2 * GRID_SIZE // 3), 2)
                elif self.direction == Direction.RIGHT:
                    pygame.draw.circle(surface, BLACK, (rect.x + 2 * GRID_SIZE // 3, rect.y + GRID_SIZE // 3), 2)
                    pygame.draw.circle(surface, BLACK, (rect.x + 2 * GRID_SIZE // 3, rect.y + 2 * GRID_SIZE // 3), 2)
            else:  # Body
                surface.blit(self.body_image, rect)
                
        # Draw shield if active
        if self.shield_active:
            head = self.get_head_position()
            shield_rect = pygame.Rect((head[0] * GRID_SIZE - 2, head[1] * GRID_SIZE - 2), 
                                      (GRID_SIZE + 4, GRID_SIZE + 4))
            pygame.draw.rect(surface, (0, 255, 255), shield_rect, 2)

class Strawberry:
    def __init__(self):
        self.position = (0, 0)
        self.image = load_image("strawberry")
        self.randomize_position()
    
    def randomize_position(self, snake_positions=None, invaders=None, powerups=None):
        if snake_positions is None:
            snake_positions = []
        if invaders is None:
            invaders = []
        if powerups is None:
            powerups = []
            
        invader_positions = [(inv.grid_x, inv.grid_y) for inv in invaders]
        powerup_positions = [p.get_grid_position() for p in powerups]
        
        all_occupied = snake_positions + invader_positions + powerup_positions
        
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in all_occupied:
                self.position = (x, y)
                break
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        surface.blit(self.image, rect)

class Invader:
    def __init__(self):
        self.grid_x = random.randint(0, GRID_WIDTH - 1)
        self.grid_y = 0  # Start at the top
        self.image = load_image("invader")
        self.speed = INVADER_SPEED
        
    def move(self):
        self.grid_y += self.speed / SNAKE_SPEED
        
        # Check if the invader has reached the bottom
        if int(self.grid_y) >= GRID_HEIGHT:
            return False
        return True
        
    def get_position(self):
        return (int(self.grid_x), int(self.grid_y))
    
    def draw(self, surface):
        rect = pygame.Rect((self.grid_x * GRID_SIZE, int(self.grid_y) * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        surface.blit(self.image, rect)
        
    def fire(self):
        if random.random() < INVADER_FIRE_RATE:
            bullet_pos = (self.grid_x * GRID_SIZE + GRID_SIZE // 2, 
                         int(self.grid_y) * GRID_SIZE + GRID_SIZE)
            return Bullet(bullet_pos, 1)  # 1 for downward direction
        return None

class Bullet:
    def __init__(self, position, direction):
        self.x, self.y = position
        self.direction = direction  # 1 for down (invader), -1 for up (snake)
        self.speed = 5
        self.width = 4
        self.height = 10
        self.image = load_image("bullet", (self.width, self.height))
        
    def move(self):
        self.y += self.direction * self.speed
        
        # Check if bullet is off-screen
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            return False
        return True
        
    def draw(self, surface):
        rect = pygame.Rect((self.x - self.width // 2, self.y - self.height // 2), 
                          (self.width, self.height))
        surface.blit(self.image, rect)
        
    def get_rect(self):
        return pygame.Rect((self.x - self.width // 2, self.y - self.height // 2), 
                          (self.width, self.height))

class PowerUp:
    def __init__(self, powerup_type):
        self.type = powerup_type
        self.grid_x = random.randint(0, GRID_WIDTH - 1)
        self.grid_y = 0  # Start at the top
        self.speed = INVADER_SPEED * 0.8  # Slightly slower than invaders
        self.active_time = 10 * SNAKE_SPEED  # Active for 10 seconds
        
        if powerup_type == PowerUpType.SPEED:
            self.image = load_image("speed_powerup")
        elif powerup_type == PowerUpType.SHIELD:
            self.image = load_image("shield_powerup")
        else:  # PowerUpType.BULLET
            self.image = load_image("bullet_powerup")
            
    def move(self):
        self.grid_y += self.speed / SNAKE_SPEED
        
        # Check if the powerup has reached the bottom
        if int(self.grid_y) >= GRID_HEIGHT:
            return False
        return True
        
    def get_grid_position(self):
        return (int(self.grid_x), int(self.grid_y))
    
    def draw(self, surface):
        rect = pygame.Rect((self.grid_x * GRID_SIZE, int(self.grid_y) * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        surface.blit(self.image, rect)

def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (40, 40, 40), rect, 1)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_game_over_screen(surface, score):
    surface.fill(BLACK)
    draw_text(surface, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, RED)
    draw_text(surface, f"Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(surface, "Press SPACE to play again or Q to quit", 24, 
              SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(10)

def show_start_screen(surface):
    surface.fill(BLACK)
    draw_text(surface, "COSMIC SNAKE", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, GREEN)
    draw_text(surface, "Arrow keys to move, SPACE to shoot", 24, 
              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(surface, "Collect strawberries and avoid invaders", 22, 
              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
    draw_text(surface, "Press SPACE to start", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(10)

def main():
    show_start_screen(screen)
    
    while True:
        # Initialize game objects
        snake = Snake()
        strawberry = Strawberry()
        invaders = []
        bullets = []
        powerups = []
        
        score = 0
        level = 1
        
        # Difficulty increases with level
        invader_spawn_rate = INVADER_SPAWN_RATE
        invader_speed_multiplier = 1.0
        
        game_over = False
        
        # Main game loop
        while not game_over:
            clock.tick(SNAKE_SPEED + (snake.speed_boost > 0) * 5)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_SPACE:
                        bullet = snake.shoot()
                        if bullet:
                            bullets.append(bullet)
                    elif event.key == pygame.K_p:
                        # Pause functionality
                        draw_text(screen, "PAUSED", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        pygame.display.flip()
                        paused = True
                        while paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif pause_event.type == pygame.KEYDOWN:
                                    if pause_event.key == pygame.K_p:
                                        paused = False
                            clock.tick(5)
            
            # Move snake
            if not snake.move():
                if not snake.shield_active:  # Shield protects from self-collision
                    game_over = True
                    continue
                    
            # Update powerups
            snake.update_powerups()
                
            # Check if snake eats the strawberry
            if snake.get_head_position() == strawberry.position:
                snake.grow()
                score += 10
                strawberry.randomize_position(snake.positions, invaders, powerups)
                
                # Level up after every 5 strawberries
                if score % 50 == 0:
                    level += 1
                    invader_spawn_rate += 0.01
                    invader_speed_multiplier += 0.2
            
            # Spawn invaders
            if len(invaders) < MAX_INVADERS and random.random() < invader_spawn_rate:
                invaders.append(Invader())
                
            # Spawn powerups (10% chance every time an invader is added)
            if random.random() < 0.1 and random.random() < invader_spawn_rate:
                powerup_type = random.choice(list(PowerUpType))
                powerups.append(PowerUp(powerup_type))
            
            # Move invaders and handle collisions
            for invader in invaders[:]:
                if not invader.move():
                    invaders.remove(invader)
                    continue
                    
                # Check if invader hits the snake
                if invader.get_position() == snake.get_head_position():
                    if snake.shield_active:
                        invaders.remove(invader)
                        score += 5
                    else:
                        game_over = True
                        break
                
                # Invaders can fire bullets
                bullet = invader.fire()
                if bullet:
                    bullets.append(bullet)
            
            # Move powerups and handle collisions
            for powerup in powerups[:]:
                if not powerup.move():
                    powerups.remove(powerup)
                    continue
                    
                # Check if snake collects powerup
                if powerup.get_grid_position() == snake.get_head_position():
                    if powerup.type == PowerUpType.SPEED:
                        snake.activate_speed_boost()
                    elif powerup.type == PowerUpType.SHIELD:
                        snake.activate_shield()
                    elif powerup.type == PowerUpType.BULLET:
                        snake.activate_bullet_powerup()
                    
                    powerups.remove(powerup)
                    score += 15
            
            # Move bullets and handle collisions
            for bullet in bullets[:]:
                if not bullet.move():
                    bullets.remove(bullet)
                    continue
                    
                bullet_rect = bullet.get_rect()
                
                # Check if bullet hits an invader (only snake bullets, which go up)
                if bullet.direction < 0:
                    for invader in invaders[:]:
                        invader_rect = pygame.Rect(
                            invader.grid_x * GRID_SIZE, 
                            int(invader.grid_y) * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE
                        )
                        
                        if bullet_rect.colliderect(invader_rect):
                            bullets.remove(bullet)
                            invaders.remove(invader)
                            score += 20
                            break
                            
                # Check if bullet hits the snake (only invader bullets, which go down)
                elif bullet.direction > 0:
                    for i, pos in enumerate(snake.positions):
                        snake_rect = pygame.Rect(
                            pos[0] * GRID_SIZE, 
                            pos[1] * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE
                        )
                        
                        if bullet_rect.colliderect(snake_rect):
                            if i == 0 and snake.shield_active:
                                # Shield protects the head from bullets
                                bullets.remove(bullet)
                                break
                            else:
                                game_over = True
                                break
            
            # Draw everything
            screen.fill(BLACK)
            # draw_grid(screen)  # Optional, for debugging
            
            strawberry.draw(screen)
            
            for invader in invaders:
                invader.draw(screen)
                
            for powerup in powerups:
                powerup.draw(screen)
                
            for bullet in bullets:
                bullet.draw(screen)
                
            snake.draw(screen)
            
            # Draw UI
            draw_text(screen, f"Score: {score}", 24, 100, 10)
            draw_text(screen, f"Level: {level}", 24, SCREEN_WIDTH - 100, 10)
            
            # Draw powerup indicators
            if snake.speed_boost > 0:
                draw_text(screen, "SPEED!", 20, SCREEN_WIDTH // 2 - 100, 10, BLUE)
                
            if snake.shield_active:
                draw_text(screen, "SHIELD!", 20, SCREEN_WIDTH // 2, 10, (0, 255, 255))
                
            if snake.can_shoot:
                draw_text(screen, "BULLETS!", 20, SCREEN_WIDTH // 2 + 100, 10, YELLOW)
            
            pygame.display.flip()
        
        # Game over - show the final screen
        show_game_over_screen(screen, score)

if __name__ == "__main__":
    main() 