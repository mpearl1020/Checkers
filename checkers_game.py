import pygame
import sys
import os
import time
from PIL import Image
from checker_board import Board

'''
This sets the position of the game window.
'''
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

pygame.init()

'''
The dimensions of the pygame surface and the caption are set.
'''
surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Checkers')

'''
Setup for the title screen text
'''
start = True
start_font = pygame.font.SysFont('verdana', 100, bold=True)
start_text = start_font.render('CHECKERS', True, (0, 0, 0))
start_rect = start_text.get_rect()
start_rect.center = (400, 300)
dir_font = pygame.font.SysFont('verdana', 60)
dir_text = dir_font.render('Press Space to Play', True, (0, 0, 0))
dir_rect = dir_text.get_rect()
dir_rect.center = (400, 400)

'''
This block allows the start window to change to the gameplay when the space
bar is pressed.
'''
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False

        surface.fill((255, 255, 255))
        surface.blit(start_text, start_rect)
        surface.blit(dir_text, dir_rect)
        pygame.display.update()

surface.fill((0, 0, 0))
board = Board()
board.initialize_game()

game_in_progress = True
turn = 'USER'
selected_piece = False
click = 0
saved_pos = {}
mouse_clicked = True

'''
This is the main game loop. The loop starts by checking to see if the game is
over (if either the user or CPU has run out of pieces). If the current turn is
the user's, then the logic below allows for the player to click on only a red
piece and have the available moves for that piece be highlighted in blue. If
the user clicks one of the newly highlighted squares, the update_board method
from the Board class is called to change the state of the game board. If it is
the CPU's turn, the move is determined by cpu_next_move() in the Board class.
A delay of 1 second is added so that the CPU's move does not occur too fast
and the user does not miss it. If either the user or the CPU wins, a new screen
appears declaring the winner and prompts the user to press the space bar if
they choose to play a new game. Otherwise, they can exit out of the window,
which terminates the program. Note that this loop is where the redrawing for
each of the screens occurs, which calls various methods from checker_board.py.
'''
while game_in_progress:
    if board.num_user_pieces == 0 or board.num_cpu_pieces == 0:
        game_in_progress = False
    if turn == 'USER':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if click == 2:
                    click = 0
                if click == 1:
                    x1, y1 = event.pos
                    new_row = y1 // 100
                    new_col = x1 // 100
                    new_piece = board.get_board_val(new_row, new_col)
                    if new_piece is not None and \
                       (new_piece.get_type() == 'USER' or
                            piece.get_type() == 'USER_KING'):
                        click = 0
                    if (((new_row, new_col), False) in positions or
                            ((new_row, new_col), True) in positions):
                        board.board = board.update_board(
                            saved_pos.get('original_row'),
                            saved_pos.get('original_col'), new_row, new_col)
                        board.reset_squares(surface)
                        board.draw(surface)
                        saved_pos = {}
                        click = 2
                        turn = 'CPU'
                if click == 0:
                    x, y = event.pos
                    row = y // 100
                    col = x // 100
                    saved_pos.update({'original_row': row})
                    saved_pos.update({'original_col': col})
                    piece = board.get_board_val(row, col)
                    type = piece.get_type()
                    check_user = type == 'USER' or type == 'USER_KING'
                    if piece is not None and (check_user):
                        board.reset_squares(surface)
                        click = 1
                        positions = board.space_available(piece)
                        for position in positions:
                            row = position[0][0]
                            col = position[0][1]
                            b = (0, 186, 255)
                            c = col * 100
                            r = row * 100
                            surface.fill(b, rect=(c, r, 100, 100))
    elif turn == 'CPU':
        if board.num_cpu_pieces != 0:
            time.sleep(1)
            move = board.cpu_next_move()
            board.update_board(move[0], move[1], move[2], move[3])
            board.reset_squares(surface)
            board.draw(surface)
            turn = 'USER'
    surface.fill((0, 65, 0), rect=(800, 0, 400, 800))
    board.draw(surface)
    pygame.display.flip()

    winner = board.check_game_over()
    win_font = pygame.font.SysFont('verdana', 100, bold=True)

    if winner == 'USER':
        win_text = win_font.render('YOU WIN!', True, (0, 0, 0))
    else:
        win_text = win_font.render('CPU WINS!', True, (0, 0, 0))

    win_rect = win_text.get_rect()
    win_rect.center = (400, 300)
    replay_font = pygame.font.SysFont('verdana', 60)
    bl = (0, 0, 0)
    replay_text = replay_font.render('Press Space to Play Again', True, bl)
    replay_rect = replay_text.get_rect()
    replay_rect.center = (400, 400)

    while not game_in_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board = Board()
                    board.initialize_game()
                    surface.fill((0, 0, 0))
                    turn = 'USER'
                    game_in_progress = True
                    break
            surface.fill((255, 255, 255))
            surface.blit(win_text, win_rect)
            surface.blit(replay_text, replay_rect)
            pygame.display.update()
