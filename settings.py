import pygame


scale = 3.5
tile_size = scale * 16
grid_w, grid_h = 20, 15
WIDTH, HEIGHT = grid_w * tile_size, grid_h * tile_size
fps = 30
magic_pixel = scale/3.5

highest_level = 0

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Seaside Signals")
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

comic_sans_font = pygame.font.SysFont("comicsansms", 50)
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
        clock.tick()


def dying(mode, draw_func, *draw_par):
    frame = 10 if mode == "in" else 0
    step = 1
    while (mode == "in" and frame < 20) or (mode == "out" and frame < 10):
        draw_func(*draw_par)
        screen.blit(death[0 if mode=="out" else 1][frame - (10 if mode=="in" else 0)], (0, 0))
        pygame.display.update()
        frame += step
        pygame.time.delay(40)


starting_img = [loadify(f"Assets/Art/backgrounds/starting_level{i}.png", scale) for i in range(4)]

starting_screen = loadify(f"Assets/Art/backgrounds/starting_screen.png", scale)

water = [loadify(f"Assets/Art/backgrounds/water{i + 1}.png", scale) for i in range(2)]

balloon = loadify(f"Assets/Art/balloon.png", scale)

boulder = [[loadify(f"Assets/Art/boulder/boulder{i}.png", scale * (0.5 if j == 1 else 1)) for i in range(2)] for j in
           range(2)]

signal = [loadify(f"Assets/Art/signal/signal{i}.png", scale) for i in range(4)]

death = [[loadify(f"Assets/Art/death/deathframe{j*10 + i + 1}.png", scale) for i in range(10)] for j in range(2)]

ground = loadify(f"Assets/Art/backgrounds/ground.png", scale)

level_imgs = [loadify(f"Assets/Art/backgrounds/level_{i}.png", scale) for i in range(7)]

dialoge_boulder_water = loadify(f"Assets/Art/dialogue/dialogue_boulder_water.png", scale)
dialoge_button_plate = loadify(f"Assets/Art/dialogue/dialogue_button_plate.png", scale)
dialoge_door_needs_signal = loadify(f"Assets/Art/dialogue/dialogue_door_needs_signal.png", scale)
dialoge_find_better_signal = loadify(f"Assets/Art/dialogue/dialogue_find_better_signal.png", scale)
dialoge_look_around = loadify(f"Assets/Art/dialogue/dialogue_look_around_first_before_coming_back.png", scale)
dialoge_look_for = loadify(f"Assets/Art/dialogue/dialogue_look_for_parts.png", scale)
dialoge_rock_block_arrow = loadify(f"Assets/Art/dialogue/dialogue_rock_block_arrow.png", scale)

code_block = [[loadify("Assets/Art/code_block/code_block" + ("_cave" if j else "") + str(i) +".png", 3*scale/4) for i in range(2)] for j in range(2)]
print(code_block)
code_shade = loadify("Assets/Art/code_block/code_shade.png", 7*scale/8)
pause_button = loadify("Assets/Art/buttons/pause_button.png", 3*scale/4)

start = loadify("Assets/Art/buttons/start.png", scale)
exit = loadify("Assets/Art/buttons/exit.png", scale)
resume = loadify("Assets/Art/buttons/resume.png", scale)
restart = loadify("Assets/Art/buttons/restart.png", scale)
map = loadify("Assets/Art/buttons/map.png", scale)
button = [loadify("Assets/Art/button.png", scale)]

pause_screen = loadify("Assets/Art/backgrounds/pause.png", scale)
shade = loadify("Assets/Art/shade.png", scale)

level_0_fix = loadify("Assets/Art/backgrounds/level_0_fix.png", scale)
level_1_fix = loadify("Assets/Art/backgrounds/level_1_fix.png", scale)
level_2_fix = loadify("Assets/Art/backgrounds/level_2_fix.png", scale)


bg_endgame = [loadify(f"Assets/Art/endgame/bg{i}.png", scale) for i in range(2)]
end_background = [loadify(f"Assets/Art/endgame/end{i}.png", scale) for i in range(2)]

cloth = loadify("Assets/Art/endgame/cloth.png", scale)
convert = loadify("Assets/Art/endgame/convert.png", scale)

temp_arrow = [loadify(f"Assets/Art/arrow/arrow{i+1}.png", scale*1.25) for i in range(3)]
arrow_imgs = []
for i in range(4):
    arrow_imgs.append([])
    for j in range(3):
        arrow_imgs[i].append(pygame.transform.rotate(temp_arrow[j], 90*(2-i)))
    arrow_imgs[i] += [loadify(f"Assets/Art/arrow/arrow4.png", scale*1.25), pygame.transform.rotate(loadify(f"Assets/Art/arrow/arrow4.png", scale*1.25), 90)]
# arrow_imgs.append([loadify(f"Assets/Art/arrow/arrow4.png", scale*1.25), pygame.transform.rotate(loadify(f"Assets/Art/arrow/arrow4.png", scale*1.25), 90)])



state = ["walk", "idle"]
directions = ["left", "back", "right", "front"]
rotation = ["left", "up", "right", "down"]


player_img = []
for i in range(3):
    player_img.append([])
    if i != 2:
        for j in range(4):
            player_img[i].append([])
            for k in range(2):
                player_img[i][j].append(
                    loadify(f"Assets/Art/character-sprites/{directions[j]}-{state[i]}-{k + 1}.png", scale))
    else:
        for j in range(3):
            player_img[i].append(loadify(f"Assets/Art/character-sprites/transmit-{j + 1}.png", scale))

door_imgs = []
for i in range(3):
    door_imgs.append([])
    for j in range(3):
        door_imgs[i].append(loadify(f"Assets/Art/door/door_{rotation[i]}{j}.png", scale))
        print(f"Assets/Art/door/door_{rotation[i]}{j}.png")
# LEGEND
# a,b,c,d = arrow directions
# e,f,g,h = laser directions
# m,n,o,p = conveyor directions

# a, b, c, d = e, f, g, h = m, n, o, p = rotation[0], rotation[1], rotation[2], rotation[3]  # arrow, laser, conveyer
a, b, c, d = 10, 11, 12, 13
e, f, g, h = 20, 21, 22, 23
m, n, o, p = 30, 31, 32, 33

q, r, w, t = 40, 41, 42, 43 # box groups

z, zg = 100, 101 #button

level_select0 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 92, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 94, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 91, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 93, 1, 0, 0, 0, 0, 0, 0, 0, 0, 90, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
]
level_select1 = [
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 95, 0, 0, 0, 96, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 912, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1]
]
level_select2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
]
level_select3 = [
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 911, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 99, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 910, 1, 0],
    [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 97, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 98, 1],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
]

level0 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 7, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, q, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, q, q, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 5, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, d, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 3, q, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, q, q, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 3, r, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, r, r, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 7, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1, 1.1, 1, 1.1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 0, 0, 0, d, 0, 0, 7, 0, 0, d, 0, 0, 7, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, 0, 4, 0, 0, 4, 0, 3, 4, 0, 3, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 5, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 7, 0, 0, b, 0, 0, 7, 0, 0, b, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1, 1.1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 4, 4, 4, 7, 4, 4, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 1, 1],
    [1, 1, 0, 3, t, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 1, 1],
    [1, 1, 0, t, t, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, 3, w, 0, 0, 0, 0, 0, 0, 0, 4, a, 0, 0, 0, 4, 1, 1],
    [1, 1, 0, w, w, 0, 0, 0, 0, 0, 0, 0, 4, a, 4, 4, 4, 4, 1, 1],
    [1, 1, 0, 3, r, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 1, 1],
    [1, 1, 0, r, r, 0, 0, 0, 0, 0, 0, 0, 4, 4, 7, 4, 0, 4, 1, 1],
    [1, 1, 0, 3, q, 0, 0, 0, 1, 1, 0, 0, 4, 4, 4, 4, 0, 4, 1, 1],
    [1, 1, 0, q, q, 0, 0, 0, 1, 1, 0, 0, 4, 4, 4, 4, 0, 4, 1, 1],
    [1, 1, 0, 0, 0, 0, b, b, 1, 1, b, b, 4, 4, 4, 4, 0, 0, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level4 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 7, 0, 0, 0, 0, 0, 0, 0, a, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 3, q, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, q, q, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 3, r, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, r, r, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 0, 1, 1, 7, 0, 0, 0, a, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level5 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, d, 2, 0, 1, z, zg, 1, d, d, d, d, d, d, d, d, d, 1, 1],
    [1, 1, 0, 0, 0, 1, zg, zg, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 7, 1, 1],
    [1, 1, 0, 3, q, 1, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, q, q, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 4, 0, 0, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1],
    [1, 1, 0, 0, 0, 4, 0, 0, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1],
    [1, 1, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 3, 0, 4, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1],
    [1, 1, 0, 0, 0, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level6 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1, 1.1, 1, 1.1, 1, 1.1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, d, 0, 0, 0, 0, 0, d, 0, d, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 3, r, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, a, 1, 1],
    [1, 1, 0, 0, r, r, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 2, 0, 3, 0, 3, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 5, 1, 1],
    [1, 1, 0, 3, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 3, q, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, q, q, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, a, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, b, 0, b, 0, 0, 0, b, 0, b, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

level_select = [level_select0, level_select1, level_select2, level_select3]
levels = [level0, level1, level2, level3, level4, level5, level6]
#"select 0": [ground, water, balloon]
level_backgrounds = {"select 0": [starting_img[0]], "select 1": [starting_img[1]], "select 2": [starting_img[2]], "select 3": [starting_img[3]],"play 0": [level_imgs[0]], "play 1": [level_imgs[1], level_1_fix], "play 2": [level_imgs[2], level_2_fix], "play 3": [level_imgs[3]], "play 4": [level_imgs[4]], "play 5": [level_imgs[5]], "play 6": [level_imgs[6]]}
level_score = [1, 1, 4, 3, 2, 1, 4]
level_spawns = [{"topright": (2, 17), "btmright": (11, 16)},
                {"topleft":(2, 2), "btmleft":(11, 1), "btmmiddle":(12, 8), "btmright":(13, 15)},
                {"spawn":(8, 10), "topright":(1, 17), "btmright":(11, 17)},
                {"btmleft":(11, 0), "topleft":(1, 8), "topright":(0, 15)}]
box_groups = {q: "g1", r: "g2", w: "g3", t: "g4"}


def loadify_sound(filename, name):
    if name == "sound":
        return pygame.mixer.Sound(filename)
    elif name == "music":
        return pygame.mixer.music.load(filename)


sfx = [f"Assets/Audio/arrow.wav", f"Assets/Audio/blockpush.wav", f"Assets/Audio/Death.wav", f"Assets/Audio/door_unlock.wav",
       f"Assets/Audio/radio_signal.wav", f"Assets/Audio/talking.wav", f"Assets/Audio/Buttonclick.wav", f"Assets/Audio/gothrough_door.wav", f"Assets/Audio/footstepjungle.wav"]
sound_List = []
for i in range(len(sfx)):
    s = loadify_sound(sfx[i], "sound")
    sound_List.append(s)

sound_List[0].set_volume(0.2)

loadify_sound(f"Assets/Audio/title_theme.mp3", "music")

def play_sound(num, sound_num=-1):
    if sound_num==-1:
        sound_num = num
    pygame.mixer.Channel(num).play(sound_List[sound_num])


pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.5)
