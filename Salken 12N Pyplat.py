import pygame, sys, os

WIDTH, HEIGHT, GRAVITY, JUMP_STRENGTH, FPS = 800, 600, 0.5, 10, 60
PLAYER_SIZE, OBSTACLE_SIZE, BORDER_THICKNESS = (32, 32), (80, 10), 10
DECELERATION, ACCELERATION, MAX_VELOCITY = 0.5, 1, 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def load_animation_frames(folder_name):
    frames = []
    folder_path = f"frames/{folder_name}"
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                frames.append(pygame.image.load(os.path.join(folder_path, filename)).convert_alpha())
    return frames

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - PLAYER_SIZE[1], *PLAYER_SIZE)
        self.velocity_y = 0
        self.velocity_x = 0
        self.acceleration_x = 0
        self.on_ground = False
        self.jumping = False
        self.double_jumped = False
        self.animations = {
            "idle": load_animation_frames("Idle"),
            "run": load_animation_frames("Run"),
            "jump": load_animation_frames("Jump"),
            "falling_down": load_animation_frames("Downfall"),
            "falling_up": load_animation_frames("Upfall"),
            "jump_peak": load_animation_frames("Apex"),
        }
        self.current_animation = "idle"
        self.current_frame = 0
        self.frame_counter = 0
        self.frames_per_animation = 10
        self.space_held = False

    def update(self, keys, obstacles, ground):
        self.acceleration_x = 0
        if keys[pygame.K_LEFT]:
            self.acceleration_x = -ACCELERATION
        elif keys[pygame.K_RIGHT]:
            self.acceleration_x = ACCELERATION
        else:
            self.acceleration_x = -DECELERATION if self.velocity_x > 0 else DECELERATION if self.velocity_x < 0 else 0
        self.velocity_x += self.acceleration_x
        self.velocity_x = max(min(self.velocity_x, MAX_VELOCITY), -MAX_VELOCITY)
        self.rect.x += self.velocity_x

        if keys[pygame.K_SPACE] and not self.space_held:
            if self.on_ground:
                self.velocity_y = -JUMP_STRENGTH
                self.jumping = True
                self.on_ground = False
                self.double_jumped = False
            elif not self.on_ground and not self.double_jumped:
                self.velocity_y = -JUMP_STRENGTH
                self.jumping = True
                self.double_jumped = True
            self.space_held = True
        elif not keys[pygame.K_SPACE]:
            self.space_held = False

        if not self.on_ground:
            self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.check_collisions(obstacles, ground)
        self.update_animation()
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_animation:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.frame_counter = 0

    def update_animation(self):
        if self.jumping:
            if self.velocity_y > 0:
                self.set_animation("falling_down")
            elif self.velocity_y == 0:
                self.set_animation("jump_peak")
            else:
                self.set_animation("falling_up")
        elif self.on_ground:
            if self.velocity_x == 0:
                self.set_animation("idle")
            else:
                self.set_animation("run")

    def set_animation(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_counter = 0

    def check_collisions(self, obstacles, ground):
        self.on_ground = False
        for obs in obstacles:
            if self.rect.colliderect(obs.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = obs.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = obs.rect.bottom
                    self.velocity_y = 0
        if self.rect.colliderect(ground.rect):
            self.rect.bottom = ground.rect.top
            self.velocity_y = 0
            self.on_ground = True
            self.jumping = False
        elif self.velocity_y > 0:
            self.on_ground = False

    def draw(self, surface):
        frames = self.animations[self.current_animation]
        offset_x, offset_y = (self.rect.width - frames[self.current_frame].get_width()) // 2, (self.rect.height - frames[self.current_frame].get_height()) // 2
        surface.blit(
            pygame.transform.flip(frames[self.current_frame], True, False) if self.velocity_x < 0 else frames[self.current_frame],
            (self.rect.x + offset_x, self.rect.y + offset_y)
        )

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *OBSTACLE_SIZE)

class Ground:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

def main():
    player = Player()
    obstacles = [Obstacle(300, HEIGHT - 150), Obstacle(500, HEIGHT - 300), Obstacle(200, HEIGHT - 400)]
    ground = Ground(0, HEIGHT - 50, WIDTH, 50)

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        player.update(keys, obstacles, ground)

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, BORDER_THICKNESS, HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT))

        player.draw(screen)
        for obs in obstacles: pygame.draw.rect(screen, (255, 0, 0), obs.rect)
        pygame.draw.rect(screen, (0, 255, 0), ground.rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
