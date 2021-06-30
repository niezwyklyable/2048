
import pygame
from _2048.constants import WIDTH, HEIGHT, FPS, SIZES, RADIUS
from _2048.game import Game
import pickle
from _2048.db_object import DB_Object

# colors
from _2048.constants import WHITE, DARK_ORANGE, GREY, GOLD

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 game v1.1 by AW')
pygame.init()

def export_object_to_pickle(game):

    try:
        with open('_2048/db.pickle', 'rb') as file:
            games_obj = pickle.load(file)

        games_obj_updated = DB_Object(games_obj.games, game)

    except:
        games = {3: None, 4: None, 5: None, 6: None, 8: None} # totally new game (never played)
        games_obj_updated = DB_Object(games, game)

    with open('_2048/db.pickle', 'wb') as file:
        pickle.dump(games_obj_updated, file)

def main(size):
    clock = pygame.time.Clock()
    run = True
    game = Game(WIN, size)
    export_object_to_pickle(game)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

                if pos[0] > 485 and pos[0] < 585 and pos[1] < 100 and pos[1] > 75 and not game.controls_blocked:
                    game.restart_screen = True
                    game.controls_blocked = True

                if pos[0] > 400 and pos[0] < 460 and pos[1] < 100 and pos[1] > 75 and \
                    not game.controls_blocked and not game.previous_step and game.previous_board:
                    game.undo()

                if game.restart_screen:
                    if pos[0] > 425 and pos[0] < 475 and pos[1] < 500 and pos[1] > 470:
                        game.restart_screen = False
                        game.controls_blocked = False

                    if pos[0] > 120 and pos[0] < 175 and pos[1] < 500 and pos[1] > 470:
                        game.new_game()
                        export_object_to_pickle(game)

                elif game._2048:
                    if pos[0] > 370 and pos[0] < 530 and pos[1] < 500 and pos[1] > 470:
                        game.restart_screen = True

                    if pos[0] > 60 and pos[0] < 240 and pos[1] < 500 and pos[1] > 470:
                        game._2048 = False
                        game.controls_blocked = False

            if event.type == pygame.KEYDOWN:
                if not game.gameover:
                    if not game.controls_blocked:
                        if event.key == pygame.K_RIGHT:
                            game.previous_step = False
                            game.save_previous_step()
                            _, game.score = game.move_right(game.board, game.score)
                            game.check_gameover()

                            if not game.after_2048:
                                game.check_win()

                            if game.score > game.best_score:
                                game.best_score = game.score

                            export_object_to_pickle(game)

                        elif event.key == pygame.K_LEFT:
                            game.previous_step = False
                            game.save_previous_step()
                            _, game.score = game.move_left(game.board, game.score)   
                            game.check_gameover()

                            if not game.after_2048:
                                game.check_win()

                            if game.score > game.best_score:
                                game.best_score = game.score

                            export_object_to_pickle(game)

                        elif event.key == pygame.K_UP:
                            game.previous_step = False
                            game.save_previous_step()
                            _, game.score = game.move_up(game.board, game.score)
                            game.check_gameover()

                            if not game.after_2048:
                                game.check_win()

                            if game.score > game.best_score:
                                game.best_score = game.score

                            export_object_to_pickle(game)

                        elif event.key == pygame.K_DOWN:
                            game.previous_step = False
                            game.save_previous_step()
                            _, game.score = game.move_down(game.board, game.score)
                            game.check_gameover()

                            if not game.after_2048:
                                game.check_win()

                            if game.score > game.best_score:
                                game.best_score = game.score

                            export_object_to_pickle(game)

                if event.key == pygame.K_ESCAPE:
                    run = False

        game.render()

def main_screen():
    clock = pygame.time.Clock()
    run = True
    num = 1

    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

                if pos[0] > 420 and pos[0] < 450 and pos[1] < 380 and pos[1] > 350:
                    if num < len(SIZES) - 1:
                        num += 1

                if pos[0] > 145 and pos[0] < 180 and pos[1] < 380 and pos[1] > 350:
                    if num > 0:
                        num -= 1

                if pos[0] > 200 and pos[0] < 400 and pos[1] < 516 and pos[1] > 467:
                    main(SIZES[num])
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if num < len(SIZES) - 1:
                        num += 1

                if event.key == pygame.K_LEFT:
                    if num > 0:
                        num -= 1

                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER \
                   or event.key == pygame.K_SPACE:
                    main(SIZES[num])
        
        # 2048 logo
        font = pygame.font.SysFont('comisans', 80)
        text = font.render('2048', 1, GOLD)
        WIN.blit(text, (int(WIDTH / 2 - text.get_width() / 2), int(HEIGHT / 3 - 2 * text.get_height())))

        # choose size
        font = pygame.font.SysFont('comisans', 30)
        text = font.render('CHOOSE SIZE:', 1, GREY)
        WIN.blit(text, (int(WIDTH / 2 - text.get_width() / 2), int(HEIGHT / 2 - 3 * text.get_height() / 2)))

        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(str(SIZES[num]) + 'x' + str(SIZES[num]), 1, GREY)
        WIN.blit(text, (int(WIDTH / 2 - text.get_width() / 2), HEIGHT // 2))

        # left arrow
        if num > 0:
            pygame.draw.polygon(WIN, GREY, [(int(WIDTH / 3 - text.get_width() / 2), HEIGHT // 2), \
                (int(WIDTH / 3 - text.get_width() / 2), int(HEIGHT / 2 + text.get_height())), \
                (int(WIDTH / 3 - text.get_width() / 2 - text.get_height()), int(HEIGHT / 2 + text.get_height() / 2))])

        # right arrow
        if num < 4:
            pygame.draw.polygon(WIN, GREY, [(int(2 * WIDTH / 3 + text.get_width() / 2), HEIGHT // 2), \
                (int(2 * WIDTH / 3 + text.get_width() / 2), int(HEIGHT / 2 + text.get_height())), \
                (int(2 * WIDTH / 3 + text.get_width() / 2 + text.get_height()), int(HEIGHT / 2 + text.get_height() / 2))])

        # play button
        pygame.draw.rect(WIN, DARK_ORANGE, (int(WIDTH / 2 - 100), int(2 * HEIGHT / 3), 200, 50), \
            border_radius=RADIUS)

        font = pygame.font.SysFont('comisans', 40)
        text = font.render('PLAY', 1, WHITE)
        WIN.blit(text, (int(WIDTH / 2 - text.get_width() / 2), int(2 * HEIGHT / 3 + text.get_height() / 2)))

        pygame.display.update()

    pygame.quit()

main_screen()
