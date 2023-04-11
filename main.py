import pygame
pygame.mixer.init()
pygame.font.init()

clock = pygame.time.Clock()
FPS = 20

screen = pygame.display.set_mode((600, 360))
pygame.display.set_caption('MY GAME')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('images/background.jpeg').convert()
lose_bg = pygame.image.load('images/sad_frog.jpg').convert()

walk_right = [
    pygame.image.load('images/player_right/right1.png').convert_alpha(),
    pygame.image.load('images/player_right/right2.png').convert_alpha(),
    pygame.image.load('images/player_right/right3.png').convert_alpha(),
    pygame.image.load('images/player_right/right4.png').convert_alpha()
]
walk_left = [
    pygame.image.load('images/player_left/left1.png').convert_alpha(),
    pygame.image.load('images/player_left/left2.png').convert_alpha(),
    pygame.image.load('images/player_left/left3.png').convert_alpha(),
    pygame.image.load('images/player_left/left4.png').convert_alpha()
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_count = 0
bg_x = 0

player_speed = 8
player_x = 150
player_y = 210

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/Fluffing-a-Duck.mp3')
lose_sound = pygame.mixer.Sound('sounds/grustnyy-trombon.mp3')
lose_sounder = 0
bg_sound.play(-1)

square = pygame.Surface((50, 70))
square.fill('blue')

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2000)

label = pygame.font.Font('fonts/Alkatra-VariableFont_wght.ttf', 40)
lose_label = label.render('AHAHA, YOU LOSE!', False, 'Yellow')
text_color = 'white'
text_xy = (205, 160)

bullets_left = 10
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullet_label = pygame.font.Font('fonts/Alkatra-VariableFont_wght.ttf', 20)
bullets = []


gameplay = True
pointer = 0

while True:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 600, 0))
    bullet_l = bullet_label.render(f'Bullets: {bullets_left}', False, 'black')
    screen.blit(bullet_l, (20, 10))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for index, i in enumerate(ghost_list_in_game):
                screen.blit(ghost, i)
                i.x -= 9
                if i.x < -60:
                    ghost_list_in_game.pop(index)
                    pointer += 10
                if player_rect.colliderect(i):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 400:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_count == 3:
            player_count = 0
        else:
            player_count += 1

        bg_x -= 3
        if bg_x == -600:
            bg_x = 0
        lose_sounder = 0

        if bullets:
            for index, i in enumerate(bullets):
                screen.blit(bullet, (i.x, i.y))
                i.x += 10
                if i.x > 620:
                    bullets.pop(index)
                if ghost_list_in_game:
                    for index1, j in enumerate(ghost_list_in_game):
                        if i.colliderect(j):
                            ghost_list_in_game.pop(index1)
                            bullets.pop(index)
                            pointer += 10


    else:
        screen.blit(lose_bg, (0, 0))
        screen.blit(lose_label, (80, 65))
        restart_label = label.render('RESTART?', False, text_color)
        restart_label_rect = restart_label.get_rect(topleft=text_xy)
        screen.blit(restart_label, restart_label_rect)
        point_label = label.render(f'Your points: {pointer}', False, 'green')
        screen.blit(point_label, (125, 180))
        bg_sound.stop()
        if lose_sounder == 0:
            lose_sound.play()
            lose_sounder += 1

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed():
            text_color = 'red'
            text_xy = (167, 122)
        else:
            text_color = 'white'
            text_xy = (170, 125)

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            pointer = 0
            bullets_left = 10
            ghost_list_in_game.clear()
            bullets.clear()
            lose_sound.stop()
            bg_sound.play()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(602, 200)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_RSHIFT and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y + 10)))
            bullets_left -= 1

    clock.tick(FPS)

