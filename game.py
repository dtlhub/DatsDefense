import pygame
import time
import sys
from dataclasses import dataclass
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 255)


WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1300

# assume that (0, 0) is center of grid
CAMERA_COORD_X = 0
CAMERA_COORD_Y = 0
CAMERA_SPEED = 0.1
CAMERA_DELTA_X = 0
CAMERA_DELTA_Y = 0
# for spped of camera
CAMERA_PING = 0.01
LAST_PRESSED_K_DOWN = time.time()
LAST_PRESSED_K_UP = time.time()
LAST_PRESSED_K_LEFT = time.time()
LAST_PRESSED_K_RIGHT = time.time()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

# one move of mouse produces 1
# zoom in or zoom out with coef 1/ZOOM_SCALE
ZOOM = 0.3
ZOOM_SCALE = 100
BLOCK_SIZE = 20
SPRITE_SIZE = BLOCK_SIZE

# experimental buggy feature
ZOOM_CENTERED_ENABLED = False

# FOR LEFT MENU
MENU_X = 200
pygame.font.init()
FONT = pygame.font.SysFont('JetBrains Mono', 20)
@dataclass
class Button:
    name: str
    x_left: int
    y_top: int
    width: int
    height: int
    # is button checkbox
    supposed_to_be_active: bool
    is_active: bool
BUTTONS = [
    Button('Increase round', 10, 180, 180, 30, False, False),
    Button('Decrease round', 10, 220, 180, 30, False, False),
    Button('Test active', 10, 260, 180, 30, True, False),
]


# GAME_INFO assume we renew it every round
ROUND = 1337
BASE_HEALTH = 30
MAX_BASE_HEALT = 100

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
    pygame.init()

    while True:
        SCREEN.fill(BLACK)
        draw_grid()
        draw_text()
        draw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                handle_mouse_wheel(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_button(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_button_pressed(keys)
        pygame.display.update()


def handle_mouse_wheel(event):
    global ZOOM, ZOOM_SCALE, ZOOM_CENTERED_ENABLED, PLAYERS, CAMERA_COORD_X, CAMERA_COORD_Y
    x, y = pygame.mouse.get_pos()
    ZOOM += -event.y / ZOOM_SCALE
    if ZOOM_CENTERED_ENABLED:
        camera_coords = mouse_coord_to_grid(x, y)
        CAMERA_COORD_X = camera_coords[0]
        CAMERA_COORD_Y = camera_coords[1]
    for p in PLAYERS:
        p.update_sprite()


def handle_button_pressed(keys):
    global LAST_PRESSED_K_LEFT, LAST_PRESSED_K_RIGHT, LAST_PRESSED_K_UP, LAST_PRESSED_K_DOWN
    global CAMERA_PING, PLAYERS, CAMERA_COORD_Y, CAMERA_COORD_X

    now = time.time()
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


def handle_mouse_button(event):
    global BUTTONS, ROUND
    x, y = pygame.mouse.get_pos()

    def in_button(button: Button, x: int, y: int):
        return (button.x_left <= x <= button.width) and (button.y_top <= y <= button.y_top + button.height)

    for button in BUTTONS:
        if in_button(button, x, y):
            if button.name == 'Increase round':
                ROUND += 1
            if button.name == 'Decrease round':
                ROUND -= 1
            if button.name == 'Test active':
                button.is_active ^= 1


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
for i in range(10**3):
    x = randint(0, 10**2)
    y = randint(0, 10**2)
    player = Player((x, y))
    PLAYERS.append(player)


def draw_player(player: Player):
    try:
        if player.rect.x < MENU_X:
            return
        SCREEN.blit(player.image, player.rect)
    except Exception as e:
        print(e)
        # exception if player not in camera
        pass


def draw_grid():
    block_size = int(BLOCK_SIZE // ZOOM)
    x_bound, y_bound = compute_screen_bounds()
    for x in range(MENU_X, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            try:
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
            except Exception as e:
                print(e)
                continue


def draw_text():
    text_surface = FONT.render('ROUND NUMBER', False, WHITE)
    SCREEN.blit(text_surface, (10, 10))

    text_surface = FONT.render(str(ROUND), False, WHITE)
    SCREEN.blit(text_surface, (10, 50))

    text_surface = FONT.render('BASE HEALTH', False, WHITE)
    SCREEN.blit(text_surface, (10, 90))

    color_coef = BASE_HEALTH / MAX_BASE_HEALT
    if 0.75 <= color_coef <= 1:
        color = WHITE
    elif 0.35 <= color_coef < 0.75:
        color = YELLOW
    else:
        color = RED

    text_surface = FONT.render(f'{BASE_HEALTH} / {MAX_BASE_HEALT}', False, color)
    SCREEN.blit(text_surface, (10, 130))


def draw_buttons():
    global BUTTONS
    for button in BUTTONS:
        if button.supposed_to_be_active:
            if button.is_active:
                bg_color = GREEN
            else:
                bg_color = RED
        else:
            bg_color = GRAY

        rect = pygame.Rect(button.x_left, button.y_top, button.width, button.height)
        pygame.draw.rect(SCREEN, bg_color, rect, 0)
        text_surface = FONT.render(button.name, False, WHITE)
        SCREEN.blit(text_surface, (button.x_left, button.y_top))


main()
