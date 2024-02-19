import pygame
import sys
from array import array
from random import randint

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

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

# Game variables and objects
left_paddle = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_DIAMETER, BALL_DIAMETER)

left_score, right_score = 0, 0

def reset_ball():
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    return [randint(-5, 5), randint(-5, 5)]

ball_speed = reset_ball()

def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
    pygame.display.flip()

def handle_paddle_movement(keys):
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 10
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.y += 10
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 10
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.y += 10

def handle_ball_movement():
    global left_score, right_score, ball_speed

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
    if ball.left <= 0:
        right_score += 1
        score_sound.play()
        ball_speed = reset_ball()
    if ball.right >= SCREEN_WIDTH:
        left_score += 1
        score_sound.play()
        ball_speed = reset_ball()
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]
        hit_paddle_sound.play()

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys)
    handle_ball_movement()
    draw_game()
    clock.tick(60)
