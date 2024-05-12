import pygame

scale = 3.5
tile_size = scale * 16
grid_w, grid_h = 20, 15
WIDTH, HEIGHT = grid_w * tile_size, grid_h * tile_size
fps = 30

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YAY TIME")
clock = pygame.time.Clock()


def loadify(filename, scaling):
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * scaling, img.get_height() * scaling))
    return img


def image(surface, img, pos, mode="corner"):
    if mode == "center":
        surface.blit(img, (pos[0] - img.get_width() / 2, pos[1] - img.get_height() / 2))
    else:
        surface.blit(img, pos)


def text(surface, _string, f_n, color, x, y, mode):
    f = f_n
    string = f.render(_string, True, color)
    string_rect = string.get_rect()

    if mode == "corner":
        string_rect.topleft = (x, y)
    else:
        string_rect.center = (x, y)

    surface.blit(string, string_rect)


def fade(surface, mode, draw_func, *draw_par):
    fade_surf = pygame.Surface((WIDTH, HEIGHT))
    fade_surf.fill((0, 0, 0))
    alpha = 255 if mode == "in" else 0
    step = -2.5 if mode == "in" else 2.5
    while (mode == "in" and alpha >= 0) or (mode == "out" and alpha <= 255):
        fade_surf.set_alpha(alpha)
        draw_func(*draw_par)
        surface.blit(fade_surf, (0, 0))
        pygame.display.update()
        alpha += step
        pygame.time.delay(2)


starting_img = loadify("Assets/Art/backgrounds/starting_level.png", scale)

water = [loadify(f"Assets/Art/backgrounds/water{i + 1}.png", scale) for i in range(2)]

balloon = loadify(f"Assets/Art/balloon.png", scale)

boulder = [[loadify(f"Assets/Art/boulder/boulder{i}.png", scale * (0.5 if j == 1 else 1)) for i in range(2)] for j in range(2)]


signal = [loadify(f"Assets/Art/signal/signal{i}.png", scale) for i in range(4)]


ground = loadify(f"Assets/Art/backgrounds/ground.png", scale)

level0_img = loadify(f"Assets/Art/backgrounds/level_0.png", scale)

state = ["walk", "idle"]
directions = ["left", "back", "right", "front"]

player_img = []
for i in range(3):
    player_img.append([])
    if i != 2:
        for j in range(4):
            player_img[i].append([])
            for k in range(2):
                player_img[i][j].append(loadify(f"Assets/Art/character-sprites/{directions[j]}-{state[i]}-{k + 1}.png", scale))
    else:
        for j in range(3):
            player_img[i].append(loadify(f"Assets/Art/character-sprites/transmit-{j + 1}.png", scale))

level_select0 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
]

level0 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 7, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, 5, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

test = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 3, 5, 0, 0, 3, 6, 0, 4, 4, 0, 7, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 5, 5, 0, 0, 6, 6, 0, 4, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

level_select = [level_select0]
levels = [test, level0]
level_backgrounds = {"select 0": [ground, water, balloon], "play 1": [level0_img]}
box_groups = {5: "g1", 6: "g2"}
