import pygame
import time
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000

# assume that (0, 0) is center of grid
CAMERA_COORD_X = 0
CAMERA_COORD_Y = 0
CAMERA_SPEED = 0.1
CAMERA_DELTA_X = 0
CAMERA_DELTA_Y = 0
CAMERA_PING = 0.01
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
ZOOM = 0.3

# one move of mouse produces 1
# zoom in or zoom out with coef 1/ZOOM_SCALE
ZOOM_SCALE = 10
BLOCK_SIZE = 20
SPRITE_SIZE = BLOCK_SIZE

# experimental buggy feature
ZOOM_CENTERED_ENABLED = False

IMAGE = pygame.image.load("player.png").convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, coords: (int, int)):
        pygame.sprite.Sprite.__init__(self)
        p_coords = apply_camera_to_computer_coords(*coords_to_grid(x, y))
        self.image = pygame.transform.scale(IMAGE, (SPRITE_SIZE // ZOOM, SPRITE_SIZE // ZOOM))
        self.rect = self.image.get_rect(center=p_coords)
        self.x = coords[0]
        self.y = coords[1]

    def update(self):
        coords = apply_camera_to_computer_coords(*coords_to_grid(self.x, self.y))
        self.rect = self.image.get_rect(center=coords)

    def update_sprite(self):
        self.image = pygame.transform.scale(IMAGE, (SPRITE_SIZE // ZOOM, SPRITE_SIZE // ZOOM))


def main():
    global SCREEN, CLOCK, CAMERA_COORD_X, CAMERA_COORD_Y, ZOOM, CAMERA_DELTA_X, CAMERA_DELTA_Y, CAMERA_PING, PLAYERS
    LAST_PRESSED_K_DOWN = time.time()
    LAST_PRESSED_K_UP = time.time()
    LAST_PRESSED_K_LEFT = time.time()
    LAST_PRESSED_K_RIGHT = time.time()
    pygame.init()

    while True:
        SCREEN.fill(BLACK)
        draw_grid()
        for event in pygame.event.get():
            """
            if event.type == pygame.KEYDOWN:
                if event.key == ord('a'):
                    CAMERA_COORD_X -= 1
                if event.key == ord('s'):
                    # want camera to move down, so invert
                    CAMERA_COORD_Y += 1
                if event.key == ord('d'):
                    CAMERA_COORD_X += 1
                if event.key == ord('w'):
                    CAMERA_COORD_Y -= 1
            """

            if event.type == pygame.MOUSEWHEEL:
                # event.y shows up or down
                x, y = pygame.mouse.get_pos()
                ZOOM += -event.y / 10
                if ZOOM_CENTERED_ENABLED:
                    camera_coords = mouse_coord_to_grid(x, y)
                    CAMERA_COORD_X = camera_coords[0]
                    CAMERA_COORD_Y = camera_coords[1]
                for p in PLAYERS:
                    p.update_sprite()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = time.time()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (now - LAST_PRESSED_K_LEFT > CAMERA_PING):
            CAMERA_COORD_X += 1
            LAST_PRESSED_K_LEFT = now
        if keys[pygame.K_RIGHT] and now - LAST_PRESSED_K_RIGHT > CAMERA_PING:
            CAMERA_COORD_X -= 1
            LAST_PRESSED_K_RIGHT = now
        if keys[pygame.K_UP] and now - LAST_PRESSED_K_UP > CAMERA_PING:
            CAMERA_COORD_Y += 1
            LAST_PRESSED_K_UP = now
        if keys[pygame.K_DOWN] and now - LAST_PRESSED_K_DOWN > CAMERA_PING:
            CAMERA_COORD_Y -= 1
            LAST_PRESSED_K_DOWN = now
        for p in PLAYERS:
            p.update()
            draw_player(p)
        pygame.display.update()


def mouse_coord_to_grid(x: int, y: int):
    block_size = int(BLOCK_SIZE // ZOOM) #Set the size of the grid block
    return x // block_size, y // block_size


def coords_to_grid(x: int, y: int):
    """
    from coordinates to pixels
    """
    # 0, 0 -> BLOCK_SIZE//(2*ZOOM), BLOCK_SIZE//(2*ZOOM)
    # 1, 0 -> BLOCK_SIZE//(2*ZOOM) * 3, BLOCK_SIZE//(2*ZOOM)
    # 2, 0 -> BLOCK_SIZE//(2*ZOOM) * 5, BLOCK_SIZE//(2*ZOOM)

    block_size = int(BLOCK_SIZE // ZOOM) #Set the size of the grid block
    return block_size * (2 * x + 1) // 2, block_size * (2 * y + 1) // 2


def apply_camera_to_computer_coords(x: int, y: int):
    block_size = int(BLOCK_SIZE // ZOOM) #Set the size of the grid block
    camera_x, camera_y = int(block_size * CAMERA_COORD_X), int(block_size * CAMERA_COORD_Y)
    return x - camera_x, y - camera_y


def compute_screen_bounds():
    left_top = apply_camera_to_computer_coords(0, 0)
    right_bottom = apply_camera_to_computer_coords(WINDOW_WIDTH, WINDOW_HEIGHT)

    x_bound = (left_top[0], right_bottom[0])
    y_bound = (left_top[1], right_bottom[1])

    return x_bound, y_bound


PLAYERS = []
from random import randint
for i in range(10**4):
    x = randint(0, 10**3)
    y = randint(0, 10**3)
    player = Player((x, y))
    PLAYERS.append(player)


def draw_player(player: Player):
    try:
        SCREEN.blit(player.image, player.rect) # Рисуем игрока
    except Exception as e:
        print(e)
        # exception if player not in camera
        pass


def draw_grid():
    block_size = int(BLOCK_SIZE // ZOOM) #Set the size of the grid block
    x_bound, y_bound = compute_screen_bounds()
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            try:
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
            except Exception as e:
                print(e)
                continue


main()
