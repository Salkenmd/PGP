import pygame
import sys
import math

WIDTH, HEIGHT, GRAVITY, JUMP_STRENGTH, FPS = 800, 600, 0.5, 10, 60
PLAYER_SIZE, OBSTACLE_SIZE, BORDER_THICKNESS, DASH_COOLDOWN, DASH_DURATION = 50, (100, 20), 10, 2000, 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.velocity_y, self.on_ground, self.dashing, self.last_dash_time, self.dash_start_time = 0, False, 0, 0, 0
        self.dash_direction = (0, 0)

    def update(self):
        if self.dashing:
            elapsed_time = pygame.time.get_ticks() - self.dash_start_time
            if elapsed_time < DASH_DURATION:
                progress = elapsed_time / DASH_DURATION
                self.rect.x += self.dash_direction[0] * 15 * progress
                self.rect.y += self.dash_direction[1] * 15 * progress
            else:
                self.dashing = False
        else:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            if self.rect.y >= HEIGHT - PLAYER_SIZE:
                self.rect.y, self.velocity_y, self.on_ground = HEIGHT - PLAYER_SIZE, 0, True
            else: 
                self.on_ground = False

    def jump(self):
        if self.on_ground: 
            self.velocity_y = -JUMP_STRENGTH

    def move(self, dx):
        if not self.dashing: 
            self.rect.x += dx

    def dash(self, direction):
        if not self.dashing and (pygame.time.get_ticks() - self.last_dash_time) >= DASH_COOLDOWN:
            self.dashing, self.last_dash_time, self.dash_start_time = True, pygame.time.get_ticks(), pygame.time.get_ticks()
            angle = math.atan2(direction[1], direction[0])
            self.dash_direction = (math.cos(angle), math.sin(angle))

    def draw(self, surface):
        color = (0, 255, 0) if self.dashing else (0, 0, 255)
        pygame.draw.rect(surface, color, self.rect)

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *OBSTACLE_SIZE)

def main():
    player = Player()
    obstacles = [Obstacle(300, HEIGHT - 150), Obstacle(500, HEIGHT - 300), Obstacle(200, HEIGHT - 400)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        player.move(dx)

        if keys[pygame.K_SPACE]: 
            player.jump()

        if keys[pygame.K_LSHIFT]:
            direction = (0, 0)
            if keys[pygame.K_UP]: direction = (0, -1)
            elif keys[pygame.K_DOWN]: direction = (0, 1)
            if keys[pygame.K_LEFT]: direction = (-1, direction[1])
            elif keys[pygame.K_RIGHT]: direction = (1, direction[1])
            if direction != (0, 0): player.dash(direction)

        player.update()

        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                if player.velocity_y > 0:
                    player.rect.bottom = obstacle.rect.top; player.velocity_y, player.on_ground = 0, True
                elif player.velocity_y < 0:
                    player.rect.top = obstacle.rect.bottom; player.velocity_y = 0

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, BORDER_THICKNESS, HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT))

        player.draw(screen)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle.rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()