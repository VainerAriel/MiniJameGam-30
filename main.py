import sys

import pygame

from Player import Player
from Tile import Tile
from Wall import Wall
from Water import Water
from Box import Box
from Signal import Signal
from settings import *


def load_level(level):
    tiles = []
    player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_type = level[y][x]
            if tile_type == 0:
                tiles.append(Tile(x, y, tile_size, tile_size, (0, 0, 0)))
            elif tile_type == 2:
                tiles.append(Tile(x, y, tile_size, tile_size, (0, 0, 0)))
                player = Player(x, y, tile_size/2+2*scale, 3*tile_size/4-3*scale, (200, 50, 50))
            elif tile_type == 1:
                tiles.append(Wall(x, y, tile_size, tile_size, (150, 25, 150)))
            elif tile_type == 4:
                tiles.append(Water(x, y, tile_size, tile_size, (25, 25, 150)))
            elif tile_type == 3:
                tiles.append(Tile(x, y, tile_size, tile_size, (0, 0, 0)))
                tiles.append(Box(x, y, tile_size, tile_size, (50, 150, 50)))
            elif tile_type == 5:
                tiles.append(Tile(x, y, tile_size, tile_size, (0, 0, 0)))
                tiles.append(Box(x, y, tile_size, tile_size, (50, 150, 50), group="g1", sprite=boulder))
            elif tile_type == 6:
                tiles.append(Tile(x, y, tile_size, tile_size, (0, 0, 0)))
                tiles.append(Box(x, y, tile_size, tile_size, (50, 150, 50), group="g2", sprite=boulder))
            elif tile_type == 7:
                tiles.append(Signal(x, y, tile_size, tile_size, (50, 0, 50), signal))
    return player, tiles


def draw_main(player, tiles, direction, moving, frame):
    screen.blit(level0_img, (0, 0))

    # screen.blit(ground, (0, 0))
    # screen.blit(water[frame], (0, 0))
    # screen.blit(balloon, (0, 0))
    # screen.fill((255, 255, 255))
    # for tile in tiles:
    #     if type(tile) == Tile:
    #         tile.show()
    # for tile in tiles:
    #     if type(tile) == Wall:
    #         tile.show()
    # for tile in tiles:
    #     if type(tile) == Water:
    #         tile.show()

    for tile in tiles:
        if type(tile) == Box:
            if tile.leader:
                tile.show()
    for tile in tiles:
        if type(tile) == Signal:
            tile.show(clock.get_time())
            # pygame.draw.circle(screen, (150, 0, 150), (tile.rect.x+tile.rect.width/2, tile.rect.y+3*tile.rect.height/2), 2*tile_size/5)
            print(tile.recharge, tile.signal_timer)
    player.show(direction, moving)
    # pygame.draw.rect(screen, (200, 0, 0), player.rect)


def main():
    player, tiles = load_level(level1)

    direction, moving = 0, 0
    water_timer = 0
    water_frame = 0

    boxes = []
    for tile in tiles:
        if tile.group == "g1":
            boxes.append(tile)
    minim = 100, 100, None
    for box in boxes:
        if box.grid_pos.x < minim[0] or box.grid_pos.y < minim[1]:
            minim = box.grid_pos.x, box.grid_pos.y, box
    minim[2].leader = True
    fade(screen, "in", draw_main, player, tiles, direction, moving, water_frame)

    run = True
    while run:
        # dt = time.time() - last_frame
        # dt *= 30
        # last_frame = time.time()

        water_timer += clock.get_time()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade(screen, "out", draw_main, player, tiles, direction, moving, water_frame)
                run = False

        moving = 1
        if player.control:
            if keys[pygame.K_w]:
                player.set_dir(player.vel.x, -1)
                direction = 1
                moving = 0
            elif keys[pygame.K_s]:
                player.set_dir(player.vel.x, 1)
                direction = 3
                moving = 0
            else:
                player.set_dir(player.vel.x, 0)

            if keys[pygame.K_a]:
                player.set_dir(-1, player.vel.y)
                direction = 0 if player.vel.y == 0 else direction
                moving = 0
            elif keys[pygame.K_d]:
                player.set_dir(1, player.vel.y)
                direction = 2 if player.vel.y == 0 else direction
                moving = 0
            else:
                player.set_dir(0, player.vel.y)
        else:
            moving = 0

        if run:
            draw_main(player, tiles, direction, moving, water_frame)

        for tile in tiles:
            if type(tile) != Box:
                tile.update_pos()
            else:
                tile.update_pos(tiles)
            tile.update_anim(clock.get_time())

        player.update(tiles, level1, clock.get_time())


        if water_timer > 900:
            water_timer = 0
            water_frame = (water_frame + 1) % 2

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
