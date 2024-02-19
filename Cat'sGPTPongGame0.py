import pygame
import sys
from array import array

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2
BALL_SPEED = [5, -5]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Game variables
left_paddle = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
hit_paddle_sound = generate_square_wave(660, 0.1, 0.1)
score_sound = generate_square_wave(220, 0.1, 0.5)

# Scores
left_score, right_score = 0, 0

# Function to reset the game
def reset_ball(ball):
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed = BALL_SPEED.copy()
    return ball_speed

ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_DIAMETER, BALL_DIAMETER)
ball_speed = reset_ball(ball)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -10)
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.move_ip(0, 10)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -10)
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.move_ip(0, 10)

    # Ball movement
    ball.move_ip(ball_speed)
    if ball.left <= 0:
        right_score += 1
        score_sound.play()
        ball_speed = reset_ball(ball)
    if ball.right >= SCREEN_WIDTH:
        left_score += 1
        score_sound.play()
        ball_speed = reset_ball(ball)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball and paddle collision
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]
        hit_paddle_sound.play()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    # Display scores
    font = pygame.font.Font(None, 74)
    text = font.render(str(left_score), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(right_score), 1, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 275, 10))

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
sys.exit()
