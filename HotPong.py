import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_size = (700, 500)
display = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pong Hot Potato")
clock = pygame.time.Clock()

# Load images 
background_img = pygame.image.load("FarmBackground.jpg")  # Replace with "FarmBackground.jpg"
hand_left_img = pygame.image.load("HandLeft.png")  # Replace with "HandLeft.png"
hand_right_img = pygame.image.load("HandRight.png")  # Replace with "HandRight.png"
potato_img = pygame.image.load("HotPotato-1.png")  # Replace with "HotPotato-1.png"

# Scale images
background_img = pygame.transform.scale(background_img, screen_size)
hand_left_img = pygame.transform.scale(hand_left_img, (200, 200))  
hand_right_img = pygame.transform.scale(hand_right_img, (200, 200))  
potato_img = pygame.transform.scale(potato_img, (150, 150))  

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Classes
class Paddle:
    """Represents a paddle (hand) controlled by the player."""
    def __init__(self, x, y, is_left):
        self.x = x
        self.y = y
        self.width = 120  
        self.height = 120  
        self.image = hand_left_img if is_left else hand_right_img
        self.speed = 5

    def draw(self):
        # Draw the image
        display.blit(self.image, (self.x - 12, self.y - 12))  

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.y > 0:
            self.y -= self.speed
        if keys[down] and self.y < screen_size[1] - self.height:
            self.y += self.speed


class Potato:
    """Represents the hot potato (ball)."""
    def __init__(self):
        self.x = screen_size[0] // 2
        self.y = screen_size[1] // 2
        self.width = 100  # Hitbox width
        self.height = 100  # Hitbox height
        self.x_speed = random.choice([-6, 6])  
        self.y_speed = random.choice([-6, 6])

    def draw(self):
        # Draw the image
        display.blit(potato_img, (self.x - 25, self.y - 25))  

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # Bounce off top and bottom edges
        if self.y <= 0 or self.y >= screen_size[1] - self.height:
            self.y_speed *= -1

    def collide(self, paddle):
        """Checks collision with a paddle's hitbox."""
        if (self.x <= paddle.x + paddle.width and self.x + self.width >= paddle.x and
            self.y <= paddle.y + paddle.height and self.y + self.height >= paddle.y):
            self.x_speed *= -1  
            self.x_speed += random.choice([-1, 1])  


# Function to display the score
def display_score(player1_score, player2_score):
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Player 1: {player1_score}   Player 2: {player2_score}", True, black)
    display.blit(score_text, (screen_size[0] // 4, 10))


# Game Objects
player1 = Paddle(30, screen_size[1] // 2 - 60, True)  
player2 = Paddle(screen_size[0] - 150, screen_size[1] // 2 - 60, False)  
potato = Potato()
player1_score = 0
player2_score = 0

# Game Loop
game_running = True
while game_running:
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Move paddles
    player1.move(pygame.K_w, pygame.K_s)
    player2.move(pygame.K_UP, pygame.K_DOWN)

    # Move potato
    potato.move()

    # Check for collisions
    potato.collide(player1)
    potato.collide(player2)

    # Check for scoring
    if potato.x <= 0:
        player2_score += 1
        potato = Potato()  
    elif potato.x >= screen_size[0] - potato.width:
        player1_score += 1
        potato = Potato()  

    # Draw everything
    display.blit(background_img, (0, 0))  
    player1.draw()
    player2.draw()
    potato.draw()

    # Display scores
    display_score(player1_score, player2_score)

    pygame.display.update()

pygame.quit()
