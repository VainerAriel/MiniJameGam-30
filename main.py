import sys

import pygame

from Player import Player
from Tile import Tile
from Wall import Wall
from Box import Box
from settings import *


def load_level(level):
    tiles = []
    player = None
    for i in range(len(level)):
        for j in range(len(level[i])):
            tile_type = level[i][j]
            if tile_type == 0:
                tiles.append(Tile(j * tile_size, i * tile_size, tile_size, tile_size, (0, 0, 0)))
            elif tile_type == 2:
                tiles.append(Tile(j * tile_size, i * tile_size, tile_size, tile_size, (0, 0, 0)))
                player = Player(j * tile_size, i * tile_size, tile_size, tile_size, (200, 50, 50))
            elif tile_type == 1:
                tiles.append(Wall(j * tile_size, i * tile_size, tile_size, tile_size, (150, 25, 150)))
            elif tile_type == 3:
                tiles.append(Tile(j * tile_size, i * tile_size, tile_size, tile_size, (0, 0, 0)))
                tiles.append(Box(j * tile_size, i * tile_size, tile_size, tile_size, (50, 150, 50)))
    return player, tiles


def draw_main(player, tiles, direction, moving, frame):
    # screen.blit(starting_img, (0, 0))

    # screen.blit(ground, (0, 0))
    # screen.blit(water[frame], (0, 0))
    # screen.blit(balloon, (0, 0))
    screen.fill((255, 255, 255))
    for tile in tiles:
        if type(tile) == Tile:
            tile.show()
    for tile in tiles:
        if type(tile) == Wall:
            tile.show()
    for tile in tiles:
        if type(tile) == Box:
            tile.show()
            if direction == 2 and pygame.Vector2(player.rect.x, player.rect.y).distance_to(tile.pos) < tile_size*2 and player.rect.y + tile_size*0.65 > tile.pos.y and  player.rect.y < tile.pos.y + tile_size:
                pygame.draw.rect(screen, (200, 200, 0), tile.rect)
                tile.pushable = True
            else:
                tile.pushable = False
    player.show(direction, moving, clock.get_time())
    # pygame.draw.rect(screen, (200, 0, 0), player.rect)


def main():
    player, tiles = load_level(level1)

    direction, moving = 0, 0
    water_timer = 0
    water_frame = 0

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

            for tile in tiles:
                if type(tile) == Box:
                    if tile.pushable and keys[pygame.K_SPACE]:
                        tile.push = not tile.push
        else:
            moving = 0

        player.move("x")
        for tile in tiles:
            col_scale = 1
            colliding = False
            if player.collide(tile):
                colliding = True
            while player.collide(tile):
                if col_scale == 0:
                    break
                player.move("x", True, col_scale)
                col_scale -= 0.1
                player.move("x", col_scale=col_scale)

            ############################################################################### FIX HUGE BUG, FIX BOX MOVING
            if type(tile) == Box and tile.push:
                print("yay")
                tile.rect = pygame.Rect(player.pos.x + tile_size+1, tile.pos.y, tile.size.x, tile.size.y)
            # if type(tile) == Box and colliding:
            #     # player.control = False
            #     player.vel.y = 0
            #     x, y = tile.pos.x//tile_size, tile.pos.y//tile_size
            #     print(x, y)
            #     tile.pos = tile.pos.lerp(pygame.Vector2((x+1)*tile_size, y*tile_size), 0.125*(1-tile.pos.distance_to(pygame.Vector2((x+1)*tile_size, y*tile_size))/tile_size/2))
            #     tile.rect = pygame.Rect(tile.pos.x, tile.pos.y, tile.size.x, tile.size.y)
            #     if tile.pos.distance_to(pygame.Vector2((x+1)*tile_size, y*tile_size)) < 2.5:
            #         tile.move(x + (1 if player.vel.x > 0 else -1), y)
            #         player.control = True

        player.move("y")
        for tile in tiles:
            col_scale = 1
            colliding = False
            if player.collide(tile):
                colliding = True
            while player.collide(tile):
                if col_scale == 0:
                    break
                player.move("y", True, col_scale)
                col_scale -= 0.1
                player.move("y", col_scale=col_scale)

            if type(tile) == Box and colliding:
                x, y = tile.pos.x // tile_size, tile.pos.y // tile_size
                tile.move(x, y + (1 if player.vel.y > 0 else -1))

        for tile in tiles:
            if type(tile) == Box:
                pass
                # print(tile.pos.x // (16*scale), tile.pos.y // (16*scale))

        if run:
            draw_main(player, tiles, direction, moving, water_frame)

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
