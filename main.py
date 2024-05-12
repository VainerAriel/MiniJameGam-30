import sys

from Arrow import Arrow, Laser
from Box import Box
from Player import Player
from Tile import Tile
from settings import *


def load_level(level, score_needed=0, spawn=None):
    tiles = []
    boxes = []
    player = None
    if spawn:
        player = Player(spawn[1], spawn[0], tile_size / 2 + 2 * scale, 3 * tile_size / 4 - 3 * scale, (200, 50, 50),
                        score_needed)
        print("yayyyy")

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
                if not spawn:
                    player = Player(x, y, tile_size / 2 + 2 * scale, 3 * tile_size / 4 - 3 * scale, (200, 50, 50),
                                    score_needed)

            elif tile_type == 3:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                box = Box(x, y, tile_size, tile_size, (50, 150, 50), tile_type="box", group="leader")
                tiles.append(tile)
                boxes.append(box)

            elif tile_type == 4:
                tile = Tile(x, y, tile_size, tile_size, (25, 25, 150), tile_type="water", fill=False, collider=True)
                tiles.append(tile)

            elif tile_type == 5:
                # door
                direction = 1
                if level[y][x + 1] != 1:
                    direction = 0
                elif level[y][x - 1] != 1:
                    direction = 2
                print(direction)

                tile = Tile(x - 1, y, tile_size, tile_size, (25, 25, 150), hit_box=(tile_size, 0) if direction == 2 else (0,0), tile_type="door",
                            fill=False, collider=True, sprites=door_imgs[direction])
                tiles.append(tile)


            elif tile_type == 7:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="signal", fill=False,
                            sprites=signal,
                            frame_limit=4, timer_limit=500)
                tiles.append(tile)

            elif tile_type in [q, r, s, t]:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                box = Box(x, y, tile_size, tile_size, (50, 150, 50), tile_type="box", group=box_groups[tile_type],
                          sprite=boulder)
                tiles.append(tile)
                boxes.append(box)

            elif tile_type in [a, b, c, d]:
                tile = Arrow(x, y, tile_size, tile_size, (150, 150, 25), tile_type="arrow",
                             direction=int(str(tile_type)[1]), bullet_sprites=arrow_imgs[int(str(tile_type)[1])])
                tiles.append(tile)

            elif tile_type in [e, f, g, h]:
                tile = Laser(x, y, tile_size, tile_size, (200, 75, 100), tile_type="laser",
                             direction=int(str(tile_type)[1]))
                tiles.append(tile)
            elif int(str(tile_type)[0]) == 9:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0), tile_type="teleporter", collider=True, value=int(str(tile_type)[1:]))
                tiles.append(tile)

    return tiles, boxes, player


def draw_main(tiles, boxes, player, frame, current_play, shapes=False):
    if not shapes:
        background_images = level_backgrounds[current_play]
        bg_img = background_images[0]
        screen.blit(bg_img, (0, 0))
        for tile in tiles:
            if tile.tile_type == "signal":
                tile.show(clock.get_time())
            if tile.tile_type == "door":
                tile.show()
        for tile in tiles:
            if tile.tile_type == "arrow":
                tile.show()
            if tile.tile_type == "laser":
                tile.setup_laser(tiles + boxes)
                tile.show(player=player)
            # if tile.tile_type == "door":
                # pygame.draw.rect(screen, (255, 0, 0), (tile.rect))
        # pygame.draw.rect(screen, (255, 150, 20), (player.rect))
        if len(background_images) > 1:
            for img in background_images[1:]:
                if type(img) == list:
                    screen.blit(img[frame], (0, 0))
                else:
                    screen.blit(img, (0, 0))
    else:
        screen.fill((255, 255, 255))
        for tile in tiles:
            if tile.tile_type == "floor":
                tile.show()

    if shapes:
        for tile in tiles:
            if tile.tile_type in ["wall", "water"]:
                tile.show()

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


def main(current_mode, current_level, current_level_select, death=False, spawn=None):
    shapes = False
    currently_displayed = level_select[current_level_select] if current_mode == "select" else levels[current_level]
    current_play = current_mode + " " + str(current_level_select if current_mode == "select" else current_level)
    tiles, boxes, player = load_level(currently_displayed,
                                      level_score[current_level] if current_mode == "play" else 0, spawn=spawn)

    water_timer, water_frame = 0, 0

    for box in boxes:
        if box.group == "leader":
            box_directions = [(1, 0), (0, 1)]
            found = False
            for d in box_directions:
                tile = currently_displayed[int(box.grid_pos.y + d[0])][int(box.grid_pos.x + d[1])]

                if tile in list(box_groups.keys()):
                    found = True
                    tile_group = box_groups[tile]
                    box.group = tile_group
                    box.leader = True
            if not found:
                box.group = ""
                box.leader = True
                box.big = False
            box.sprites = box.sprites[0 if box.big else 1]

    for tile in tiles:
        if tile.tile_type == "laser":
            tile.setup_laser(tiles)

    door = None
    for tile in tiles:
        if tile.tile_type == "door":
            door = tile

    if not death:
        fade(screen, "in", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
    else:
        dying("in", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
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

        if current_mode == "play":
            if door:
                future_rect = pygame.Rect(player.rect.x + (player.vel.x * player.speed),
                                          player.rect.y + (player.vel.y * player.speed),
                                          player.size.x, player.size.y)
                door_hitbox = pygame.Rect(door.rect.x + door.hit_box[0],
                                          door.rect.y+ door.hit_box[1],
                                          tile_size, tile_size)
                print(future_rect)
                print(door_hitbox)
                if future_rect.colliderect(door_hitbox):
                    fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
                    return 0, False

            if player.dead:
                dying("out", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
                return 0, True
            for tile in tiles:
                if tile.tile_type != "box":
                    tile.update_pos()

                if tile.tile_type == "arrow":
                    tile.shoot(clock.get_time(), tiles + boxes, player)
                tile.update_anim(clock.get_time())

            for box in boxes:
                box.update_pos(tiles)

        else:
            spawn_point = None
            if current_level_select == 0:
                if player.rect.x > WIDTH:
                    if player.rect.y < HEIGHT / 2:
                        spawn_point = level_spawns[1]["topleft"], 1
                    else:
                        spawn_point = level_spawns[1]["btmleft"], 1
                elif player.rect.y > HEIGHT:
                    spawn_point = level_spawns[2]["topright"], 2
            elif current_level_select == 1:
                if player.rect.x + player.rect.width < 0:
                    if player.rect.y < HEIGHT / 2:
                        spawn_point = level_spawns[0]["topright"], 0
                    else:
                        spawn_point = level_spawns[0]["btmright"], 0
                elif player.rect.y > HEIGHT:
                    if player.rect.x < WIDTH / 2:
                        spawn_point = level_spawns[3]["topleft"], 3
                    else:
                        spawn_point = level_spawns[3]["topright"], 3
            elif current_level_select == 2:
                if player.rect.y + player.rect.height < 0:
                    spawn_point = level_spawns[0]["btmright"], 0
                elif player.rect.x > WIDTH:
                    spawn_point = level_spawns[3]["btmleft"], 3
            else:
                if player.rect.x + player.rect.width < 0:
                    spawn_point = level_spawns[2]["btmright"], 2
                elif player.rect.y + player.rect.height < 0:
                    if player.rect.x < WIDTH / 2:
                        spawn_point = level_spawns[1]["btmmiddle"], 1
                    else:
                        spawn_point = level_spawns[1]["btmright"], 1
            if spawn_point is not None:
                fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
                return 1, spawn_point

        player.update(tiles + boxes, clock.get_time())

        if player.teleport:
            fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, shapes)
            return 2, player.level

        if water_timer > 900:
            water_timer = 0
            water_frame = (water_frame + 1) % 2

        if run:
            draw_main(tiles, boxes, player, water_frame, current_play, shapes)

        pygame.display.update()
        clock.tick(fps)


def draw_main_menu(btn):
    screen.blit(starting_screen, (0, 0))
    pygame.draw.rect(screen, (50, 200, 50), btn)
    # screen.fill((50, 50, 200))


def main_menu():
    btn = pygame.Rect(WIDTH*3/4-WIDTH/6, HEIGHT/2+HEIGHT/6, WIDTH/3, HEIGHT/6)
    btn2 = pygame.Rect(WIDTH*3/4-WIDTH/6, HEIGHT/2+HEIGHT/6, WIDTH/3, HEIGHT/6)

    current_mode = "select"
    current_level, current_level_select = 0, 2
    spawn_point = level_spawns[2]["spawn"]

    fade(screen, "in", draw_main_menu, btn)
    state = "main menu"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if state == "game":
            game = main(current_mode, current_level, current_level_select, spawn=(spawn_point if current_mode == "select" else None))
            if game[0] == 0:
                dead = game[1]
                while dead:
                    dead = main(current_mode, current_level, current_level_select, death=True)
                current_mode = "select"

            elif game[0] == 1:
                spawn_point, current_level_select = game[1]

            else:
                current_level = game[1]
                current_mode = "play"

            #fade(screen, "in", draw_main_menu, btn)
        else:
            draw_main_menu(btn)
        if btn.collidepoint(mx, my) and click:
            state = "game"
            fade(screen, "out", draw_main_menu, btn)

        clock.tick(fps)
        pygame.display.update()


main_menu()
