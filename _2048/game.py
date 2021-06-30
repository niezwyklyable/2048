
import pygame
from .constants import WIDTH, MARGIN, HEIGHT, RADIUS, GAP, PROBABILITY

# colors
from .constants import WHITE, GREY, WHITE_WITH_ALPHA, GOLD_WITH_ALPHA, LIGHT_GREY
from .tile import Tile
import random
from copy import deepcopy
import pickle

class Game():
    BOARD_SIZE = WIDTH - 2 * MARGIN

    def __init__(self, win, size):
        self.win = win
        self.size = size
        self.tile_size = (self.BOARD_SIZE - GAP * (self.size + 1)) // self.size
        self.start_values = []

        for i in range(100):
            if i < PROBABILITY:
                self.start_values.append(4)
            else:
                self.start_values.append(2)

        try:
            with open('_2048/db.pickle', 'rb') as file:
                games_obj = pickle.load(file)
                games = games_obj.games

        except:
            games = {3: None, 4: None, 5: None, 6: None, 8: None} # totally new game (never played)

        if games[self.size]:
            self.board, self.score, self.best_score, self.previous_score, \
            self.previous_board, self.previous_step, self.restart_screen, self.gameover, \
            self._2048, self.controls_blocked, self.after_2048 = games_obj.get_last_game(self.size)
        
        else:
            self.best_score = 0
            self.new_game()

    def new_game(self):
        self.score = 0
        self.previous_score = 0
        self.previous_board = []
        self.previous_step = False
        self.restart_screen = False
        self.gameover = False
        self._2048 = False
        self.controls_blocked = False
        self.after_2048 = False
        self.create_board()
        starting_tiles = self.create_tile(self.board)
        starting_tiles.update(self.create_tile(self.board)) # metoda IN-PLACE - zwraca None
        self.create_visualization(starting_tiles)

    def create_board(self):
        self.board = [[0 for _ in range(0, self.size)] for _ in range(0, self.size)]

        for row in range(self.size):
            for col in range(self.size):
                self.board[row][col] = Tile(row, col, self.tile_size, 0)

    def render(self):
        self.win.fill(WHITE)

        font = pygame.font.SysFont('comicsans', 70)
        text_2048 = font.render('2048', 1, GREY)
        self.win.blit(text_2048, (MARGIN, int((HEIGHT - WIDTH) / 2 - text_2048.get_height() / 2)))

        font = pygame.font.SysFont('comicsans', 30)
        text = font.render('RESTART', 1, GREY)
        self.win.blit(text, (int(WIDTH - MARGIN - text.get_width()), int(HEIGHT - WIDTH - MARGIN)))

        font = pygame.font.SysFont('comicsans', 30)
        text2 = font.render('UNDO', 1, GREY)
        self.win.blit(text2, (int(WIDTH - MARGIN - text.get_width() - 3 * text2.get_width() / 2), int(HEIGHT - WIDTH - MARGIN)))

        pygame.draw.rect(self.win, GREY, (400, int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height()), \
            60, 60), border_radius = RADIUS)
        font = pygame.font.SysFont('comicsans', 18)
        text_score = font.render('SCORE', 1, WHITE)
        self.win.blit(text_score, (int(430 - text_score.get_width() / 2),\
           int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height() / 2)))
        font = pygame.font.SysFont('comicsans', 22)
        score = font.render(str(self.score), 1, WHITE)
        self.win.blit(score, (int(430 - score.get_width() / 2),\
           int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height() + 35)))

        pygame.draw.rect(self.win, GREY, (480, int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height()), \
            100, 60), border_radius = RADIUS)
        font = pygame.font.SysFont('comicsans', 18)
        text_best_score = font.render('BEST SCORE', 1, WHITE)
        self.win.blit(text_best_score, (int(530 - text_best_score.get_width() / 2),\
           int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height() / 2)))
        font = pygame.font.SysFont('comicsans', 22)
        best_score = font.render(str(self.best_score), 1, WHITE)
        self.win.blit(best_score, (int(530 - best_score.get_width() / 2),\
           int(HEIGHT - WIDTH - 3.5 * MARGIN - text.get_height() + 35)))

        self.draw_board()
        self.draw_tiles()

        if self.gameover:
            s = pygame.Surface((self.BOARD_SIZE, self.BOARD_SIZE), pygame.SRCALPHA)
            s.fill(WHITE_WITH_ALPHA)
            self.win.blit(s, (MARGIN, HEIGHT - WIDTH + MARGIN))
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render('GAME OVER!', 1, GREY)
            self.win.blit(text, (int(WIDTH / 2 - text.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + self.BOARD_SIZE / 2 - text.get_height() / 2)))

        if self._2048:
            s = pygame.Surface((self.BOARD_SIZE, self.BOARD_SIZE), pygame.SRCALPHA)
            s.fill(GOLD_WITH_ALPHA)
            self.win.blit(s, (MARGIN, HEIGHT - WIDTH + MARGIN))
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render('YOU WIN!', 1, WHITE)
            self.win.blit(text, (int(WIDTH / 2 - text.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + self.BOARD_SIZE / 2 - text.get_height() / 2)))
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render('KEEP GOING', 1, WHITE)
            self.win.blit(text, (int(WIDTH / 4 - text.get_width() / 2), \
                int(HEIGHT - WIDTH - MARGIN + 3 * self.BOARD_SIZE / 4 - text.get_height())))
            text = font.render('TRY AGAIN', 1, WHITE)
            self.win.blit(text, (int(3 * WIDTH / 4 - text.get_width() / 2), \
                int(HEIGHT - WIDTH - MARGIN + 3 * self.BOARD_SIZE / 4 - text.get_height())))

        if self.restart_screen:
            s = pygame.Surface((self.BOARD_SIZE, self.BOARD_SIZE), pygame.SRCALPHA)
            s.fill(WHITE_WITH_ALPHA)
            self.win.blit(s, (MARGIN, HEIGHT - WIDTH + MARGIN))
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render('RESTART?', 1, GREY)
            self.win.blit(text, (int(WIDTH / 2 - text.get_width() / 2), \
                int(HEIGHT - WIDTH + MARGIN + self.BOARD_SIZE / 2 - text.get_height() / 2)))
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render('YES', 1, GREY)
            self.win.blit(text, (int(WIDTH / 4 - text.get_width() / 2), \
                int(HEIGHT - WIDTH - MARGIN + 3 * self.BOARD_SIZE / 4 - text.get_height())))
            text = font.render('NO', 1, GREY)
            self.win.blit(text, (int(3 * WIDTH / 4 - text.get_width() / 2), \
                int(HEIGHT - WIDTH - MARGIN + 3 * self.BOARD_SIZE / 4 - text.get_height())))

        pygame.display.update()

    def move_visualization(self, items): # dodanie plynnego ruchu podczas przesuwania kafelkow
        
        for tile, step in items:
            tile.x += tile.dx
            tile.y += tile.dy

            if tile.dx < 0:
                if tile.x < tile.dest_x:
                    tile.x = tile.dest_x
            elif tile.dx > 0:
                if tile.x > tile.dest_x:
                    tile.x = tile.dest_x
            elif tile.dy < 0:
                if tile.y < tile.dest_y:
                    tile.y = tile.dest_y
            elif tile.dy > 0:
                if tile.y > tile.dest_y:
                    tile.y = tile.dest_y

        self.render()

        for tile, step in items:
            if tile.x != tile.dest_x or tile.y != tile.dest_y:
                break
        else:
            return

        self.move_visualization(items)

    def create_visualization(self, tiles_final_cond):

        for tile, fc in tiles_final_cond.items():
            tile.size += 2 * tile.dR
            tile.x -= tile.dR
            tile.y -= tile.dR

            final_x, final_y, final_size = fc
            
            if tile.size > final_size:
                tile.size = final_size
                tile.x = final_x
                tile.y = final_y

        self.render()

        for tile, fc in tiles_final_cond.items():
            final_size = fc[2]

            if tile.size != final_size:
                break
        else:
            return

        self.create_visualization(tiles_final_cond)

    def calc_cond_for_merge_visual(self, items, dir):
        EXPAND_FACTOR = 1.1
        tiles_cond = {}

        if dir == 'left':
            row_corr = 0
            col_corr = -1  
        elif dir == 'right':
            row_corr = 0
            col_corr = 1
        elif dir == 'up':
            row_corr = -1
            col_corr = 0
        elif dir == 'down':
            row_corr = 1
            col_corr = 0

        for tile, merge in items:
            if merge:
                actual_tile = self.board[tile.row + row_corr][tile.col + col_corr]
                init_x = actual_tile.x
                init_y = actual_tile.y
                init_size = self.tile_size
                final_x = int(actual_tile.x - (EXPAND_FACTOR - 1) / 2 * self.tile_size)
                final_y = int(actual_tile.y - (EXPAND_FACTOR - 1) / 2 * self.tile_size)
                final_size = int(EXPAND_FACTOR * self.tile_size)
                expand = True
                tiles_cond.update({actual_tile: \
                    [init_x, init_y, init_size, final_x, final_y, final_size, expand]})

        return tiles_cond

    def merge_visualization(self, tiles_cond):
        
        for tile, cond in tiles_cond.items():
            expand = cond[-1]

            if expand:
                tile.size += 2 * tile.dR2
                tile.x -= tile.dR2
                tile.y -= tile.dR2

                final_x, final_y, final_size = cond[3:6]
            
                if tile.size > final_size:
                    tile.size = final_size
                    tile.x = final_x
                    tile.y = final_y
            else:
                tile.size -= 2 * tile.dR2
                tile.x += tile.dR2
                tile.y += tile.dR2

                init_x, init_y, init_size = cond[:3]
            
                if tile.size < init_size:
                    tile.size = init_size
                    tile.x = init_x
                    tile.y = init_y

        self.render()

        for tile, cond in tiles_cond.items():
            expand = cond[-1]
            
            if expand:
                final_size = cond[-2]

                if tile.size == final_size:
                   tiles_cond[tile][-1] = False
                else:
                    break
        else:
            for tile, cond in tiles_cond.items():
                expand = cond[-1]
            
                if not expand:
                    init_size = cond[2]

                    if tile.size != init_size:
                        break
            else:
                return

        self.merge_visualization(tiles_cond)

    def draw_board(self):
        pygame.draw.rect(self.win, GREY, (MARGIN, HEIGHT - WIDTH + MARGIN, \
            self.BOARD_SIZE, self.BOARD_SIZE), border_radius = RADIUS)

        # na potrzeby wizualizacji (tło kafelka 0 podczas przemieszczania sie kafelkow niezerowych)
        for row in range(self.size):
            for col in range(self.size):
                pygame.draw.rect(self.win, LIGHT_GREY, (MARGIN + GAP + col * (self.tile_size + GAP), \
                    HEIGHT - WIDTH + MARGIN + GAP + row * (self.tile_size + GAP), \
                    self.tile_size, self.tile_size), border_radius = RADIUS)

    def draw_tiles(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col].value != 0:
                    self.board[row][col].draw(self.win)

    def find_empty_tiles(self, board):

        def _find_zeros(tile):
            return tile.value == 0

        empty_tiles = []

        for row in board:
            empty_tiles += list(filter(_find_zeros, row))

        return empty_tiles

    def create_tile(self, board):
        random_tile = random.choice(self.find_empty_tiles(board))
        random_value = random.choice(self.start_values)
        random_tile.value = random_value
        random_tile.size = 0
        final_x = random_tile.x
        final_y = random_tile.y
        random_tile.x += self.tile_size // 2
        random_tile.y += self.tile_size // 2
        
        return {random_tile: (final_x, final_y, self.tile_size)}

    def move_left(self, board, score):

        def _try_to_do_steps():
            # zlapanie odleglosci pierwszego kafelka od lewej krawedzi 
            # oraz odleglosci pomiedzy kafelkami w kazdym rzedzie
            tiles_steps = {} # {tile: step}

            for row in range(self.size):
                for col in range(self.size):
                    tiles_steps.update({board[row][col]: 0})
            
            for row in range(self.size):
                counter = 0

                for col in range(self.size):
                    if board[row][col].value == 0:
                        counter += 1
                        continue

                    tiles_steps[board[row][col]] = counter

            # jezeli board jest rzeczywistym boardem to dokonac wizualizacji ruchu 
            # wszystkich kafelkow rownoczesnie
            if board is self.board:
                for tile, step in tiles_steps.items():
                    tile.calc_dest('left', step)

                self.move_visualization(tiles_steps.items())

            # przesuniecie wszystkich kafelkow o te odleglosci w lewo w kazdym rzedzie
            for tile, step in tiles_steps.items():
                if step > 0:
                    old_row = tile.row
                    old_col = tile.col
                    tile.move('left', step)
                    # stworzenie nowego aliasu obiektu i nadpisanie starego nowym obiektem
                    # (zmiana pola .value w starym aliasie zmienilaby to pole rowniez w nowym !!!)
                    board[tile.row][tile.col] = board[old_row][old_col]
                    board[old_row][old_col] = Tile(old_row, old_col, self.tile_size, 0)

            return tiles_steps.values()

        steps = _try_to_do_steps()

        # dokonanie mergu wszystkich kafelkow w kazdym rzedzie o ile to mozliwe 
        # (kroki analogicznie jak wyzej)
        tiles_merge = {} # {tile: bool}

        for row in range(self.size):
            for col in range(self.size):
                tiles_merge.update({board[row][col]: False})

        for row in range(self.size):
            for col in range(1, self.size):
                if board[row][col].value == 0:
                    continue

                if not tiles_merge[board[row][col-1]] and \
                    board[row][col].value == board[row][col-1].value:
                    if board[row][col].value != 2048:
                        tiles_merge[board[row][col]] = True

        for tile, merge in tiles_merge.items():
            if merge:
                board[tile.row][tile.col-1].value *= 2
                board[tile.row][tile.col].value = 0
                score += board[tile.row][tile.col-1].value

        # ponowne przesuniecie kafelkow w przypadku dokonania merge'a
        if True in tiles_merge.values():
            _try_to_do_steps()

            if board is self.board:
                tiles_cond = self.calc_cond_for_merge_visual(tiles_merge.items(), 'left')
                self.merge_visualization(tiles_cond)

        # stworzenie nowego kafelka
        going_on = False
        
        if any(steps) or True in tiles_merge.values():
            if board is self.board:
                self.create_visualization(self.create_tile(board))

            going_on = True
            return (going_on, score)

        return (going_on, score)

    def move_right(self, board, score):

        def _try_to_do_steps():
            # zlapanie odleglosci pierwszego kafelka od prawej krawedzi 
            # oraz odleglosci pomiedzy kafelkami w kazdym rzedzie
            tiles_steps = {} # {tile: step}

            for row in range(self.size):
                for col in range(self.size):
                    tiles_steps.update({board[row][col]: 0})
            
            for row in range(self.size):
                counter = 0

                for col in range(self.size - 1, -1, -1):
                    if board[row][col].value == 0:
                        counter += 1
                        continue

                    tiles_steps[board[row][col]] = counter

            # jezeli board jest rzeczywistym boardem to dokonac wizualizacji ruchu 
            # wszystkich kafelkow rownoczesnie
            if board is self.board:
                for tile, step in tiles_steps.items():
                    tile.calc_dest('right', step)

                self.move_visualization(tiles_steps.items())

            # przesuniecie wszystkich kafelkow o te odleglosci w prawo w kazdym rzedzie
            reversed_items = list(tiles_steps.items())
            reversed_items.reverse() # metoda ta wykonuje sie tzw. IN-PLACE i zwraca None

            for tile, step in reversed_items:
                if step > 0:
                    old_row = tile.row
                    old_col = tile.col
                    tile.move('right', step)
                    # stworzenie nowego aliasu obiektu i nadpisanie starego nowym obiektem
                    # (zmiana pola .value w starym aliasie zmienilaby to pole rowniez w nowym !!!)
                    board[tile.row][tile.col] = board[old_row][old_col]
                    board[old_row][old_col] = Tile(old_row, old_col, self.tile_size, 0)
            
            return tiles_steps.values()

        steps = _try_to_do_steps()

        # dokonanie mergu wszystkich kafelkow w kazdym rzedzie o ile to mozliwe 
        # (kroki analogicznie jak wyzej)
        tiles_merge = {} # {tile: bool}

        for row in range(self.size):
            for col in range(self.size):
                tiles_merge.update({board[row][col]: False})

        for row in range(self.size):
            for col in range(self.size - 2, -1, -1):
                if board[row][col].value == 0:
                    continue

                if not tiles_merge[board[row][col+1]] and \
                    board[row][col].value == board[row][col+1].value:
                    if board[row][col].value != 2048:
                        tiles_merge[board[row][col]] = True

        for tile, merge in tiles_merge.items():
            if merge:
                board[tile.row][tile.col+1].value *= 2
                board[tile.row][tile.col].value = 0
                score += board[tile.row][tile.col+1].value

        # ponowne przesuniecie kafelkow w przypadku dokonania merge'a
        if True in tiles_merge.values():
            _try_to_do_steps()

            if board is self.board:
                tiles_cond = self.calc_cond_for_merge_visual(tiles_merge.items(), 'right')
                self.merge_visualization(tiles_cond)

        # stworzenie nowego kafelka
        going_on = False

        if any(steps) or True in tiles_merge.values():
            if board is self.board:
                self.create_visualization(self.create_tile(board))

            going_on = True
            return (going_on, score)

        return (going_on, score)

    def move_up(self, board, score):

        def _try_to_do_steps():
            # zlapanie odleglosci pierwszego kafelka od gornej krawedzi 
            # oraz odleglosci pomiedzy kafelkami w kazdej kolumnie
            tiles_steps = {} # {tile: step}

            for row in range(self.size):
                for col in range(self.size):
                    tiles_steps.update({board[row][col]: 0})
            
            for col in range(self.size):
                counter = 0

                for row in range(self.size):
                    if board[row][col].value == 0:
                        counter += 1
                        continue

                    tiles_steps[board[row][col]] = counter

            # jezeli board jest rzeczywistym boardem to dokonac wizualizacji ruchu 
            # wszystkich kafelkow rownoczesnie
            if board is self.board:
                for tile, step in tiles_steps.items():
                    tile.calc_dest('up', step)

                self.move_visualization(tiles_steps.items())

            # przesuniecie wszystkich kafelkow o te odleglosci w gore w kazdej kolumnie
            for tile, step in tiles_steps.items():
                if step > 0:
                    old_row = tile.row
                    old_col = tile.col
                    tile.move('up', step)
                    # stworzenie nowego aliasu obiektu i nadpisanie starego nowym obiektem
                    # (zmiana pola .value w starym aliasie zmienilaby to pole rowniez w nowym !!!)
                    board[tile.row][tile.col] = board[old_row][old_col]
                    board[old_row][old_col] = Tile(old_row, old_col, self.tile_size, 0)

            return tiles_steps.values()

        steps = _try_to_do_steps()

        # dokonanie mergu wszystkich kafelkow w kazdej kolumnie o ile to mozliwe 
        # (kroki analogicznie jak wyzej)
        tiles_merge = {} # {tile: bool}

        for row in range(self.size):
            for col in range(self.size):
                tiles_merge.update({board[row][col]: False})

        for col in range(self.size):
            for row in range(1, self.size):
                if board[row][col].value == 0:
                    continue

                if not tiles_merge[board[row-1][col]] and \
                    board[row][col].value == board[row-1][col].value:
                    if board[row][col].value != 2048:
                        tiles_merge[board[row][col]] = True

        for tile, merge in tiles_merge.items():
            if merge:
                board[tile.row-1][tile.col].value *= 2
                board[tile.row][tile.col].value = 0
                score += board[tile.row-1][tile.col].value

        # ponowne przesuniecie kafelkow w przypadku dokonania merge'a
        if True in tiles_merge.values():
            _try_to_do_steps()

            if board is self.board:
                tiles_cond = self.calc_cond_for_merge_visual(tiles_merge.items(), 'up')
                self.merge_visualization(tiles_cond)

        # stworzenie nowego kafelka
        going_on = False

        if any(steps) or True in tiles_merge.values():
            if board is self.board:
                self.create_visualization(self.create_tile(board))

            going_on = True
            return (going_on, score)

        return (going_on, score)

    def move_down(self, board, score):
        
        def _try_to_do_steps():
            # zlapanie odleglosci pierwszego kafelka od dolnej krawedzi 
            # oraz odleglosci pomiedzy kafelkami w kazdej kolumnie
            tiles_steps = {} # {tile: step}

            for row in range(self.size):
                for col in range(self.size):
                    tiles_steps.update({board[row][col]: 0})
            
            for col in range(self.size):
                counter = 0

                for row in range(self.size - 1, -1, -1):
                    if board[row][col].value == 0:
                        counter += 1
                        continue

                    tiles_steps[board[row][col]] = counter

            # jezeli board jest rzeczywistym boardem to dokonac wizualizacji ruchu 
            # wszystkich kafelkow rownoczesnie
            if board is self.board:
                for tile, step in tiles_steps.items():
                    tile.calc_dest('down', step)

                self.move_visualization(tiles_steps.items())

            # przesuniecie wszystkich kafelkow o te odleglosci w dol w kazdej kolumnie
            reversed_items = list(tiles_steps.items())
            reversed_items.reverse() # metoda ta wykonuje sie tzw. IN-PLACE i zwraca None

            for tile, step in reversed_items:
                if step > 0:
                    old_row = tile.row
                    old_col = tile.col
                    tile.move('down', step)
                    # stworzenie nowego aliasu obiektu i nadpisanie starego nowym obiektem
                    # (zmiana pola .value w starym aliasie zmienilaby to pole rowniez w nowym !!!)
                    board[tile.row][tile.col] = board[old_row][old_col]
                    board[old_row][old_col] = Tile(old_row, old_col, self.tile_size, 0)
            
            return tiles_steps.values()

        steps = _try_to_do_steps()

        # dokonanie mergu wszystkich kafelkow w kazdym rzedzie o ile to mozliwe 
        # (kroki analogicznie jak wyzej)
        tiles_merge = {} # {tile: bool}

        for row in range(self.size):
            for col in range(self.size):
                tiles_merge.update({board[row][col]: False})

        for col in range(self.size):
            for row in range(self.size - 2, -1, -1):
                if board[row][col].value == 0:
                    continue

                if not tiles_merge[board[row+1][col]] and \
                    board[row][col].value == board[row+1][col].value:
                    if board[row][col].value != 2048:
                        tiles_merge[board[row][col]] = True

        for tile, merge in tiles_merge.items():
            if merge:
                board[tile.row+1][tile.col].value *= 2
                board[tile.row][tile.col].value = 0
                score += board[tile.row+1][tile.col].value

        # ponowne przesuniecie kafelkow w przypadku dokonania merge'a
        if True in tiles_merge.values():
            _try_to_do_steps()

            if board is self.board:
                tiles_cond = self.calc_cond_for_merge_visual(tiles_merge.items(), 'down')
                self.merge_visualization(tiles_cond)

        # stworzenie nowego kafelka
        going_on = False

        if any(steps) or True in tiles_merge.values():
            if board is self.board:
                self.create_visualization(self.create_tile(board))

            going_on = True
            return (going_on, score)

        return (going_on, score)

    def check_gameover(self):
        temp_board = deepcopy(self.board)

        if self.move_left(temp_board, 0)[0]:
            return

        if self.move_right(temp_board, 0)[0]:
            return

        if self.move_down(temp_board, 0)[0]:
            return

        if self.move_up(temp_board, 0)[0]:
            return
        
        self.gameover = True

    def check_win(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col].value == 2048:
                    self._2048 = True
                    self.after_2048 = True
                    self.controls_blocked = True
                    return

    def undo(self):
        self.previous_step = True
        self.gameover = False
        self.score = self.previous_score
        self.board = self.previous_board

    def save_previous_step(self):
        self.previous_score = self.score
        self.previous_board = deepcopy(self.board)
