import math
import sys

import pygame.mixer

from Arrow import Arrow, Laser
from Box import Box
from Dialogue import Dialogue
from Player import Player
from Tile import Tile
from settings import *

dialogue = Dialogue(2 * tile_size, 13 * tile_size)


def load_level(level, score_needed=0, spawn=None):
    tiles = []
    boxes = []
    pressure_plates = []
    player = None
    if spawn:
        player = Player(spawn[1], spawn[0], tile_size / 2 + 2 * scale, 3 * tile_size / 4 - 3 * scale, (200, 50, 50),
                        score_needed)

    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_type = level[y][x]
            if tile_type == 0:
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0))
                tiles.append(tile)

            elif tile_type == 1:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="wall", fill=False, collider=True)
                tiles.append(tile)

            elif tile_type == 1.1:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="code block", collider=True,
                            sprites=code_block[0])
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

                tile = Tile(x - 1, y, tile_size, tile_size, (25, 25, 150),
                            hit_box=(tile_size, 0) if direction == 2 else ((-tile_size, 0) if direction == 0 else (0, 0)), tile_type="door",
                            fill=False, collider=True, sprites=door_imgs[direction])
                tiles.append(tile)


            elif tile_type == 7:
                tile = Tile(x, y, tile_size, tile_size, (150, 25, 150), tile_type="signal", fill=False,
                            sprites=signal,
                            frame_limit=4, timer_limit=500)
                tiles.append(tile)

            elif tile_type in [q, r, w, t]:
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
                tile = Tile(x, y, tile_size, tile_size, (0, 0, 0), tile_type="teleporter", collider=True,
                            value=int(str(tile_type)[1:]))
                tiles.append(tile)

            elif tile_type == z:
                tile = Tile(x, y, tile_size, tile_size, (0, 255, 0), tile_type="pressure plate", group="leader",
                            collider=False, sprites=button, frame_limit=1)
                tiles.append(tile)
                pressure_plates.append(tile)
            elif tile_type == zg:
                tile = Tile(x, y, tile_size, tile_size, (0, 255, 0), tile_type="pressure plate", group="p1",
                            collider=False, sprites=button, frame_limit=1)
                tiles.append(tile)
                pressure_plates.append(tile)

    return tiles, boxes, player, pressure_plates


def draw_main(tiles, boxes, player, frame, current_play, current_mode):
    background_images = level_backgrounds[current_play]
    bg_img = background_images[0]
    screen.blit(bg_img, (0, 0))
    for box in boxes:
        if box.leader and not box.collider:
            box.show()
    for tile in tiles:
        if tile.tile_type == "signal":
            tile.show(clock.get_time())
        if tile.tile_type == "door":
            tile.show()
        if tile.tile_type == "pressure plate" and tile.group == "leader":
            tile.show()
    for tile in tiles:
        if tile.tile_type == "arrow":
            tile.show()
        if tile.tile_type == "laser":
            tile.setup_laser(tiles + boxes)
            tile.show(player=player)
    for box in boxes:
        if box.leader and box.collider:
            box.show()
        # if tile.tile_type == "door":
        # pygame.draw.rect(screen, (255, 0, 0), (tile.rect))
    # pygame.draw.rect(screen, (255, 150, 20), (player.rect))
    if len(background_images) > 1:
        for img in background_images[1:]:
            if type(img) == list:
                screen.blit(img[frame], (0, 0))
            else:
                screen.blit(img, (0, 0))

    for tile in tiles:
        if tile.tile_type == "code block":
            screen.blit(code_shade, (tile.rect.x + tile_size / 8, tile.rect.y + tile_size / 8))
            tile.show()
    dialogue.show(clock.get_time(), pygame.key.get_pressed(), pygame.mouse.get_pressed()[0])

    player.show()

    if current_mode == "play":
        screen.blit(pause_button, (tile_size / 4, tile_size / 4))


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


def main(current_mode, current_level, current_level_select, death=False, spawn=None, score=0):
    if current_level == 0 and current_mode == "play":
        dialogue.trigger([dialoge_door_needs_signal, dialoge_find_better_signal, dialoge_boulder_water])
    if spawn == level_spawns[2]["spawn"]:
        dialogue.trigger([dialoge_look_for])
    if current_level_select == 3 and current_mode == "select" and highest_level != 7:
        dialogue.trigger([dialoge_look_around])
    if current_level == 2 and current_mode == "play":
        dialogue.trigger([dialoge_rock_block_arrow])
    if current_level == 5 and current_mode == "play":
        dialogue.trigger([dialoge_button_plate])
    currently_displayed = level_select[current_level_select] if current_mode == "select" else levels[current_level]
    current_play = current_mode + " " + str(current_level_select if current_mode == "select" else current_level)
    tiles, boxes, player, pressure_plates = load_level(currently_displayed,
                                                       level_score[current_level] if current_mode == "play" else 0,
                                                       spawn=spawn)

    water_timer, water_frame = 0, 0
    pause = False

    for box in boxes:
        if box.group == "leader":
            box_directions = [(1, 0), (0, 1)]
            found = False
            for d in box_directions:
                tile = currently_displayed[int(box.grid_pos.y + d[0])][int(box.grid_pos.x + d[1])]

                if tile in list(box_groups.keys()):
                    found = True
                    tile_group = box_groups[tile]
                    print(tile_group)
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
        fade(screen, "in", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
    else:
        dying("in", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)

    run = True
    while run:
        # dt = time.time() - last_frame
        # dt *= 30
        # last_frame = time.time()
        water_timer += clock.get_time()
        # print(pressure_plates[0].pressed)
        keys = pygame.key.get_pressed()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    play_sound(2)
                    dying("out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                    return 0, True
                if event.key == pygame.K_ESCAPE and current_mode == "play":
                    pause = not pause
                    # play_sound(2)
                    # dying("out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                    # return 0, True

        if not pause:
            player_movement(player, keys)

            if current_mode == "play":
                if door:
                    if door.open:
                        if current_level != 1:
                            door_hitbox = pygame.Rect(door.rect.x + door.hit_box[0],
                                                      door.rect.y + door.hit_box[1],
                                                      tile_size, tile_size)
                        else:
                            door_hitbox = pygame.Rect(door.rect.x,
                                                      door.rect.y,
                                                      tile_size, tile_size)
                        future_rect = pygame.Rect(player.rect.x + (player.vel.x * player.speed),
                                                  player.rect.y + (player.vel.y * player.speed),
                                                  player.size.x, player.size.y)

                        if future_rect.colliderect(door_hitbox):
                            fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                            return 0, False, current_level, True

                if player.dead:
                    play_sound(2)
                    dying("out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                    return 0, True, current_level, False
                for tile in tiles:
                    if tile.tile_type != "box":
                        tile.update_pos()

                    tile.update_button(tiles + boxes)

                    if tile.tile_type == "arrow":
                        if len(pressure_plates) > 0:
                            tile.shoot(clock.get_time(), tiles + boxes, player, pressure_plates[0].pressed)
                        else:
                            tile.shoot(clock.get_time(), tiles + boxes, player, False)
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
                    fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                    return 1, spawn_point

            player.update(tiles + boxes, clock.get_time())

            if player.teleport:
                fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                return 2, player.level

            if water_timer > 900:
                water_timer = 0
                water_frame = (water_frame + 1) % 2



        mx, my = pygame.mouse.get_pos()
        if run:
            draw_main(tiles, boxes, player, water_frame, current_play, current_mode)
            if current_mode == "play":
                if math.dist((mx, my), (tile_size, tile_size)) < 3 * tile_size / 4 and click:
                    pause = not pause

        if pause:
            screen.blit(shade, (0, 0))
            screen.blit(pause_screen, (0, 0))
            btn1 = pygame.Rect(WIDTH / 2 - resume.get_width() / 2, HEIGHT / 2 - HEIGHT / 13, resume.get_width(),
                               resume.get_height())
            btn2 = pygame.Rect(WIDTH / 2 - restart.get_width() / 2, HEIGHT / 2 - HEIGHT / 13 + HEIGHT / 6,
                               restart.get_width(), restart.get_height())
            btn3 = pygame.Rect(WIDTH / 2 - map.get_width() / 2, HEIGHT / 2 - HEIGHT / 13 + 2 * HEIGHT / 6,
                               map.get_width(), map.get_height())
            screen.blit(resume, (WIDTH / 2 - resume.get_width() / 2, HEIGHT / 2 - HEIGHT / 13))
            screen.blit(restart, (WIDTH / 2 - resume.get_width() / 2, HEIGHT / 2 - HEIGHT / 13 + HEIGHT / 6))
            screen.blit(map, (WIDTH / 2 - resume.get_width() / 2, HEIGHT / 2 - HEIGHT / 13 + 2 * HEIGHT / 6))

            if btn1.collidepoint(mx, my) and click:
                pause = not pause
            elif btn2.collidepoint(mx, my) and click:
                play_sound(2)
                dying("out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                return 0, True, current_level, False
            elif btn3.collidepoint(mx, my) and click:
                fade(screen, "out", draw_main, tiles, boxes, player, water_frame, current_play, current_mode)
                return 0, False, current_level, False

        if current_mode == "select":
            btn4 = pygame.Rect(WIDTH-bg_endgame[0].get_width()+4*scale, HEIGHT-bg_endgame[0].get_height(), bg_endgame[0].get_width(), bg_endgame[0].get_height())
            screen.blit(bg_endgame[0], (btn4.x, btn4.y))

            screen.blit(bg_endgame[0], (-40*scale, btn4.y))
            text(screen, str(score) + "   ", comic_sans_font, (255, 255, 255), (bg_endgame[0].get_width()-40*scale) / 2, btn4.y+bg_endgame[0].get_height()/2,"center")
            screen.blit(cloth, ((bg_endgame[0].get_width()-40*scale) / 2-3*scale, btn4.y+bg_endgame[0].get_height()/2-cloth.get_height()/2))
            screen.blit(convert, (btn4.x+10*magic_pixel-2*scale, btn4.y+5*magic_pixel))
            if btn4.collidepoint(mx, my) and click and score == 7:
                return [3]

        pygame.display.update()
        clock.tick(fps)

def end_draw(frame):
    screen.blit(end_background[frame], (0, 0))
def end_func():
    timer = 0
    frame = 0
    fade(screen, "in", end_draw, frame)
    while True:
        timer += clock.get_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade(screen, "out", end_draw, frame)
                pygame.quit()
                sys.exit()
        if timer > 750:
            timer = 0
            frame = (frame+1)%2
        end_draw(frame)
        pygame.display.update()
        clock.tick(fps)

def draw_main_menu(btn, btn2):
    screen.blit(starting_screen, (0, 0))
    screen.blit(start, (btn.x, btn.y))
    screen.blit(exit, (btn2.x, btn2.y))

    # screen.fill((50, 50, 200))


def main_menu():
    btn = pygame.Rect(170 * scale, 140 * scale, 96 * scale, 30 * scale)
    btn2 = pygame.Rect(170 * scale, 175 * scale, 96 * scale, 30 * scale)

    current_mode = "select"
    current_level, current_level_select = 0, 2
    spawn_point = level_spawns[2]["spawn"]

    fade(screen, "in", draw_main_menu, btn, btn2)
    state = "main menu"

    score = 0
    won = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        print(f"Won:{won}, Score:{score}")
        if state == "game":
            game = main(current_mode, current_level, current_level_select,
                        spawn=(spawn_point if current_mode == "select" else None),score=score)
            if game[0] == 0:
                dead = game[1]
                while dead:
                    dead = main(current_mode, current_level, current_level_select, death=True, score=score)[1]
                print(game)
                if len(game) >=4:
                    if game[3] and game[2] not in won:
                        won.append(game[2])
                        score += 1
                else:
                    won.append(current_level)
                    score += 1
                current_mode = "select"
                loadify_sound(f"Assets/Audio/title_theme.mp3", "music")
                pygame.mixer.music.play(-1)

            elif game[0] == 1:
                spawn_point, current_level_select = game[1]

            elif game[0] == 2:
                current_level = game[1]
                current_mode = "play"
                loadify_sound(f"Assets/Audio/jungle_theme.mp3", "music")
                pygame.mixer.music.play(-1)
            else:
                loadify_sound(f"Assets/Audio/ending_theme.mp3", "music")
                pygame.mixer.music.play(-1)
                end_func()

            # fade(screen, "in", draw_main_menu, btn)
        else:
            draw_main_menu(btn, btn2)

        if pygame.Rect(170 * scale, btn.y, btn.width, btn.height).collidepoint(mx, my):
            btn.x = btn.x + (185 * scale - btn.x) * 0.1
            if click:
                state = "game"
                play_sound(6)
                fade(screen, "out", draw_main_menu, btn, btn2)
        else:
            btn.x = btn.x + (170 * scale - btn.x) * 0.1

        if pygame.Rect(170 * scale, btn2.y, btn2.width, btn2.height).collidepoint(mx, my):
            btn2.x = btn2.x + (185 * scale - btn2.x) * 0.1
            if click:
                play_sound(6)
                fade(screen, "out", draw_main_menu, btn, btn2)
                pygame.quit()
                sys.exit()
        else:
            btn2.x = btn2.x + (170 * scale - btn2.x) * 0.1

        clock.tick(fps)
        pygame.display.update()


main_menu()
