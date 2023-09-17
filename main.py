import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Constants
WIDTH, HEIGHT = 1200, 900
GROUND_HEIGHT = 20
GAME_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goose Goose Duck Adventure")

# Load sound effect for passing a cactus
pass_cactus_sound = pygame.mixer.Sound("scoresound.mp3")  # Replace with the actual sound file

# Load the background image
background_img = pygame.image.load("bg.gif")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Resize it to fit the screen

# Load images
dino_img = pygame.image.load("goose.png")  # Replace with the actual path to your dino image
cactus_img = pygame.image.load("bus.png")  # Replace with the actual path to your cactus image

# Resize images
dino_img = pygame.transform.scale(dino_img, (300, 300))
cactus_img = pygame.transform.scale(cactus_img, (300, 500))

# Create a font object for displaying text
font = pygame.font.Font(None, 36)


# Define the Dino character
class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - GROUND_HEIGHT - 350
        self.jump = False
        self.jump_height = 0
        self.collision_tolerance = 110
        self.landed = True
        self.gravity = 1  # Adjust the gravity value as needed
        self.life = 5

    def jump_action(self):
        if not self.jump and not game_over:
            self.jump = True
            self.jump_height = 30  # Reset jump height
            self.landed = False

    def move(self):
        if self.jump:
            self.y -= self.jump_height
            self.jump_height -= 1
            if self.y >= HEIGHT - GROUND_HEIGHT - 350:
                self.jump = False
                self.y = HEIGHT - GROUND_HEIGHT - 350
                self.landed = True
        elif self.y < HEIGHT - GROUND_HEIGHT - 350:
            self.y += self.gravity  # Apply gravity when not jumping

        # Ensure Dino stays within vertical boundaries
        if self.y > HEIGHT - GROUND_HEIGHT - 350:
            self.y = HEIGHT - GROUND_HEIGHT - 350

    def draw(self):
        screen.blit(dino_img, (self.x, self.y))

    def collides_with(self, obstacle):
        if not self.landed:
            return False
        dino_mask = pygame.mask.from_surface(dino_img)
        obstacle_mask = pygame.mask.from_surface(cactus_img)
        offset = (int(obstacle.x - self.x), int(obstacle.y - self.y))
        overlap = dino_mask.overlap(obstacle_mask, offset)
        return bool(overlap)


# Define the Cactus obstacle
class Cactus:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT - GROUND_HEIGHT - 500  # Place the cactus just above the ground
        self.initial_y = self.y  # Store the initial y position
        self.scored = False  # Track if this cactus has already been scored

    def move(self):
        self.x -= GAME_SPEED

        # Ensure cactus stays within vertical boundaries
        if self.y > self.initial_y:
            self.y = self.initial_y

    def reset(self):
        self.x = WIDTH
        self.y = self.initial_y
        self.scored = False

    def draw(self):
        screen.blit(cactus_img, (self.x, self.y))

# Create Dino and Cactus objects
dino = Dino()
cactus = Cactus()

# Initialize the score
score = 0

# Starting with life
life = 5

# Define the initial score text
score_text = font.render("Score: " + str(score), True, BLACK)
life_text = font.render("Life: " + str(life), True, BLACK)

# Game loop
running = True
game_over = False
replay_requested = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over or replay_requested:  # Allow jumping and restarting
                    # Reset the game state
                    game_over = False
                    score = 0
                    life = 5
                    dino = Dino()
                    cactus = Cactus()
                    replay_requested = False
                    # Clear the game over text from the screen
                    game_over_text = None
                    # Reset the life text
                    life_text = font.render("Life: " + str(life), True, BLACK)
                else:  # If the game is not over, allow jumping
                    dino.jump_action()

    screen.fill(WHITE)

    # Draw the background image
    screen.blit(background_img, (0, 0))

    if not game_over or replay_requested:
        dino.move()
        cactus.move()

        dino.draw()
        cactus.draw()

        if cactus.x < -20:
            cactus = Cactus()

        if cactus.x + 20 < dino.x and not cactus.scored and not game_over:
            score += 1
            cactus.scored = True
            # Play the sound effect for passing a cactus
            pass_cactus_sound.play()

        # Check for collisions
        if not game_over and dino.collides_with(cactus):
            life -= 1  # Decrease life by 1 when there's a collision
            if life == 0:
                game_over = True
                dino.x = 50  # Reset the dino's position
                print("Game Over")
                replay_requested = False
            else:
                # Reset the cactus state to prevent instant collisions after a reset
                cactus.reset()

            # Reduce the life
            life_text = font.render("Life: " + str(life), True, BLACK)


    dino.draw()
    cactus.draw()


    # Update the score when the cactus passes the Dino
    if cactus.x + 20 < dino.x and not cactus.scored:
        score += 1
        cactus.scored = True

    if game_over:
        game_over_text = font.render("Game Over. Press SPACE to replay.", True, (255, 0, 0))  # Red color
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
        screen.blit(game_over_text, text_rect)
    score_text = font.render("Score: " + str(score), True, BLACK)
    life_text = font.render("Life: " + str(life), True, BLACK)


    screen.blit(score_text, (20, 20))
    screen.blit(life_text, (20, 60))

    pygame.display.flip()
    pygame.time.delay(20)

    # Allow the player to replay by resetting the game state
    if replay_requested and pygame.key.get_pressed()[pygame.K_SPACE]:
        # Reset the game state
        game_over = False
        score = 0
        life = 5
        dino = Dino()
        cactus = Cactus()
        replay_requested = False  # Reset replay request

# Close Pygame and exit
pygame.quit()
sys.exit()
