import sys

from Box import Box
from Player import Player
from Tile import Tile
from settings import *


def load_level(level):
    tiles = []
    boxes = []
    player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_type = level[y][x]
            if tile_type == 0:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                tiles.append(tile)

            elif tile_type == 1:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="wall", fill=False, collider=True)
                tiles.append(tile)

            elif tile_type == 2:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                tiles.append(tile)
                player = Player(x, y, tile_size / 2 + 2 * scale, 3 * tile_size / 4 - 3 * scale, (200, 50, 50))

            elif tile_type == 3:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                box = Box(x, y, tile_size, tile_size, (50, 150, 50), tile_type="box", group="leader")
                tiles.append(tile)
                boxes.append(box)

            elif tile_type == 4:
                tile = Tile(x, y, tile_size, tile_size, (25, 25, 150), tile_type="water", fill=False, collider=True)
                tiles.append(tile)

            elif tile_type in [5, 6]:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                box = Box(x, y, tile_size, tile_size, (50, 150, 50), tile_type="box", group=box_groups[tile_type], sprite=boulder[0])
                tiles.append(tile)
                boxes.append(box)

            elif tile_type == 7:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="signal", fill=False, sprites=signal,
                            frame_limit=4, timer_limit=500)
                tiles.append(tile)

    return tiles, boxes, player


def draw_main(tiles, boxes, player, frame, current_play, shapes=False):
    if not shapes:
        background_images = level_backgrounds[current_play]
        for img in background_images:
            if type(img) == list:
                screen.blit(img[frame], (0, 0))
            else:
                screen.blit(img, (0, 0))
    else:
        screen.fill((255, 255, 255))
        for tile in tiles:
            if tile.tile_type == "floor":
                tile.show()
        for tile in tiles:
            if tile.tile_type in ["wall", "water"]:
                tile.show()

    for tile in tiles:
        if tile.tile_type == "signal":
            tile.show(clock.get_time())
    for box in boxes:
        if box.leader:
            box.show()
    player.show()


def player_movement(player, keys):
    player.moving = 1
    if player.control:
        if keys[pygame.K_w]:
            player.set_dir(player.vel.x, -1)
            player.direction = 1
            player.moving = 0
        elif keys[pygame.K_s]:
            player.set_dir(player.vel.x, 1)
            player.direction = 3
            player.moving = 0
        else:
            player.set_dir(player.vel.x, 0)

        if keys[pygame.K_a]:
            player.set_dir(-1, player.vel.y)
            player.direction = 0 if player.vel.y == 0 else player.direction
            player.moving = 0
        elif keys[pygame.K_d]:
            player.set_dir(1, player.vel.y)
            player.direction = 2 if player.vel.y == 0 else player.direction
            player.moving = 0
        else:
            player.set_dir(0, player.vel.y)
    else:
        player.moving = 0


def main():
    current_level = 0
    current_level_select = 0
    current_mode = "play"
    shapes = current_level == 0 and current_mode == "play"

    currently_displayed = level_select[current_level_select] if current_mode == "select" else levels[current_level]
    current_play = current_mode + " " + str(current_level_select if current_mode == "select" else current_level)
    tiles, boxes, player = load_level(currently_displayed)

    water_timer, water_frame = 0, 0

    for box in boxes:
        if box.group == "leader":
            box_directions = [(1, 0), (0, 1)]
            for d in box_directions:
                tile = currently_displayed[int(box.grid_pos.y + d[0])][int(box.grid_pos.x + d[1])]

                if tile in list(box_groups.keys()):
                    tile_group = box_groups[tile]
                    box.group = tile_group
                    box.leader = True

    fade(screen, "in", draw_main, tiles, boxes, player, water_frame, current_play, shapes)

    run = True
    while run:
        # dt = time.time() - last_frame
        # dt *= 30
        # last_frame = time.time()
        water_timer += clock.get_time()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
                run = False

        player_movement(player, keys)

        for tile in tiles:
            if tile.tile_type != "box":
                tile.update_pos()
            tile.update_anim(clock.get_time())

        for box in boxes:
            box.update_pos(tiles)

        player.update(tiles+boxes, clock.get_time())

        if water_timer > 900:
            water_timer = 0
            water_frame = (water_frame + 1) % 2

        if run:
            draw_main(tiles, boxes, player, water_frame, current_play, shapes)

        pygame.display.update()
        clock.tick(fps)


def draw_main_menu(btn):
    screen.fill((50, 50, 200))
    pygame.draw.rect(screen, (50, 200, 50), btn)


def main_menu():
    btn = pygame.Rect(500, 400, 200, 100)
    fade(screen, "in", draw_main_menu, btn)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        draw_main_menu(btn)
        if btn.collidepoint(mx, my) and click:
            fade(screen, "out", draw_main_menu, btn)
            main()
            fade(screen, "in", draw_main_menu, btn)
        clock.tick(fps)
        pygame.display.update()


main()
