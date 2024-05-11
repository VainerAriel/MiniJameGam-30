import sys

from Player import Player
from Tile import Tile
from Wall import Wall
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
    return player, tiles


def draw_main(player, tiles, direction, moving):
    screen.blit(starting_img, (0, 0))
    # screen.fill((255, 255, 255))
    # for tile in tiles:
    #     tile.show()
    print(clock.get_time())
    player.show(direction, moving, clock.get_time())


def main():
    player, tiles = load_level(level0)

    direction, moving = 0, 0

    fade(screen, "in", draw_main, player, tiles, direction, moving)

    run = True
    while run:
        # dt = time.time() - last_frame
        # dt *= 30
        # last_frame = time.time()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade(screen, "out", draw_main, player, tiles, direction, moving)
                run = False

        moving = 1

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

        player.move("x")
        for tile in tiles:
            col_scale = 1
            while player.collide(tile):
                if col_scale == 0:
                    break
                player.move("x", True, col_scale)
                col_scale -= 0.1
                player.move("x", col_scale=col_scale)

        player.move("y")
        for tile in tiles:
            col_scale = 1
            while player.collide(tile):
                if col_scale == 0:
                    break
                player.move("y", True, col_scale)
                col_scale -= 0.1
                player.move("y", col_scale=col_scale)

        if run:
            draw_main(player, tiles, direction, moving)

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
