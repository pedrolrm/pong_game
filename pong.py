"""
This script recreates the classic and iconic Pong game originally developed by Atari in the 70s.
It uses the Pygame library to handle graphics, input, and game logic.
The game features two paddles controlled by players, 
a ball that bounces off the paddles and the screen edges,
and a scoring system to keep track of each player's points.
"""
import sys
import pygame

# Initializing Pygame
pygame.init()

# Setting up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setting up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Setting up the clock
clock = pygame.time.Clock()

# Score counters
player1_score = 0
player2_score = 0

class Paddle:
    """
    Class representing a paddle in the Pong game.
    
    Attributes:
        rect (pygame.Rect): The rectangle representing the paddle's position and size.
    """
    def __init__(self, x, y):
        """
        Initialize a paddle.
        
        Args:
            x (int): The x-coordinate of the paddle.
            y (int): The y-coordinate of the paddle.
        """
        self.rect = pygame.Rect(x, y, 10, 100)

    def move(self, y):
        """
        Move the paddle vertically.
        
        Args:
            y (int): The number of pixels to move the paddle by.
        """
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball:
    """
    Class representing the ball in the Pong game.
    
    Attributes:
        rect (pygame.Rect): The rectangle representing the ball's position and size.
        speed_x (int): The horizontal speed of the ball.
        speed_y (int): The vertical speed of the ball.
    """
    def __init__(self, x, y):
        """
        Initialize the ball.
        
        Args:
            x (int): The x-coordinate of the ball.
            y (int): The y-coordinate of the ball.
        """
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        """
        Move the ball according to its speed and handle collisions with the screen edges.
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

def reset_ball():
    """
    Reset the ball to the center of the screen and reverse its horizontal direction.
    """
    ball.rect.x = SCREEN_WIDTH // 2 - ball.rect.width // 2
    ball.rect.y = SCREEN_HEIGHT // 2 - ball.rect.height // 2
    ball.speed_x = -ball.speed_x

def draw_dashed_line(surface, color, x, dash_length, gap_length):
    """
    Draw a dashed line vertically down the center of the screen.
    
    Args:
        surface (pygame.Surface): The surface to draw the line on.
        color (tuple): The color of the line.
        x (int): The x-coordinate of the line.
        dash_length (int): The length of each dash.
        gap_length (int): The length of each gap between dashes.
    """
    for y in range(0, SCREEN_HEIGHT, dash_length + gap_length):
        pygame.draw.line(surface, color, (x, y), (x, y + dash_length))

# Initializing paddles and ball
player1 = Paddle(30, SCREEN_HEIGHT // 2 - 50)
player2 = Paddle(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - 50)
ball = Ball(SCREEN_WIDTH // 2 - 7, SCREEN_HEIGHT // 2 - 7)

# Paddle speed
PADDLE_SPEED = 10

def main():
    """
    The main game loop. 
    Handles events, updates game state, and draws the game elements on the screen.
    """
    global player1_score, player2_score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            player1.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            player2.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            player2.move(PADDLE_SPEED)

        ball.move()

        # Ball collision with paddles
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.speed_x = -ball.speed_x

        # Updating scores
        if ball.rect.left <= 0:
            player2_score += 1
            reset_ball()
        if ball.rect.right >= SCREEN_WIDTH:
            player1_score += 1
            reset_ball()

        # Drawing elements on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1.rect)
        pygame.draw.rect(screen, WHITE, player2.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        draw_dashed_line(screen, WHITE, SCREEN_WIDTH // 2, 10, 10)

        # Drawing the score
        font = pygame.font.Font(None, 74)
        text = font.render(str(player1_score), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 4, 10))
        text = font.render(str(player2_score), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH * 3 // 4, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
