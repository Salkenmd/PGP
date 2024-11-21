import pygame
import sys

WIDTH, HEIGHT, GRAVITY, JUMP_STRENGTH, FPS = 800, 600, 0.5, 10, 60
PLAYER_SIZE, OBSTACLE_SIZE = 50, (100, 20)
BORDER_THICKNESS = 10  # Thickness of the borders

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.velocity_y, self.on_ground = 0, False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= HEIGHT - PLAYER_SIZE:
            self.rect.y, self.velocity_y, self.on_ground = HEIGHT - PLAYER_SIZE, 0, True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground: self.velocity_y = -JUMP_STRENGTH

    def move(self, dx):
        self.rect.x += dx

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *OBSTACLE_SIZE)

def main():
    player = Player()
    obstacles = [Obstacle(300, HEIGHT - 150), Obstacle(500, HEIGHT - 300), Obstacle(200, HEIGHT - 400)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5)
        if keys[pygame.K_SPACE]: player.jump()
        player.update()

        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                if player.velocity_y > 0:
                    player.rect.bottom = obstacle.rect.top
                    player.velocity_y = 0
                    player.on_ground = True
                elif player.velocity_y < 0:
                    player.rect.top = obstacle.rect.bottom
                    player.velocity_y = 0

        screen.fill((255, 255, 255))

        #borders
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, BORDER_THICKNESS))  #top border
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, BORDER_THICKNESS, HEIGHT))  #left border
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS))  #bottom border
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT))  #right border

        #player and obstacles
        pygame.draw.rect(screen, (0, 0, 255), player.rect)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle.rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()