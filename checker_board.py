import pygame
import os
from random import randrange
from PIL import Image
from piece import Piece

'''
The Board class contains all of the logic for the checkers game (specific
functions will be detailed below). A Board object contains information such as
the board array, the number of user and cpu pieces remaining and the winner.
'''


class Board:
    '''
    This is the constructor to instantiate a Board object by initializing the
    instance variables defined above.
    '''
    def __init__(self):
        self.board = None
        self.num_user_pieces = 12
        self.num_cpu_pieces = 12
        self.winner = None

    '''
    This function takes in a pygame surface object and is responsible for
    drawing the black and red squares and the yellow dividing lines. It also
    displays the Piece icons by iterating through the board array and
    determining the coordinates of each piece.
    '''
    def draw(self, surface):
        for i in range(8):
            for j in range(8):
                if self.get_board_val(i, j):
                    pos = (j * 100 + 5, i * 100 + 5)
                    if self.get_board_val(i, j) == Piece('CPU', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), pos)
                    elif self.get_board_val(i, j) == Piece('USER', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), pos)
                    elif self.get_board_val(i, j) == Piece('CPU_KING', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), pos)
                    elif self.get_board_val(i, j) == Piece('USER_KING', i, j):
                        surface.blit(self.get_board_val(i, j).get_icon(), pos)
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 0:
                    rectangle = (j, 100 * i, 100, 100)
                    surface.fill((255, 0, 0), rect=rectangle)
                else:
                    rectangle = (j + 100, 100 * i, 100, 100)
                    surface.fill((255, 0, 0), rect=rectangle)
        for i in range(100, 800, 100):
            pygame.draw.line(surface, (255, 233, 0), (0, i), (800, i), 2)
            pygame.draw.line(surface, (255, 233, 0), (i, 0), (i, 800), 2)
        pygame.draw.line(surface, (255, 233, 0), (0, 0), (0, 800), 5)
        pygame.draw.line(surface, (255, 233, 0), (0, 800), (800, 800), 5)
        pygame.draw.line(surface, (255, 233, 0), (800, 800), (800, 0), 5)
        pygame.draw.line(surface, (255, 233, 0), (800, 0), (0, 0), 5)

        surface.fill((0, 65, 0), rect=(800, 0, 400, 800))

    '''
    This function is responsible for drawing the red squares on the checker
    board.
    '''
    def draw_squares(self, surface):
        red = (255, 0, 0)
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 0:
                    surface.fill(red, rect=(j, 100 * i, 100, 100))
                else:
                    surface.fill(red, rect=(j + 100, 100 * i, 100, 100))

    '''
    This function resets squares to black after they are set to blue and the
    user switches the currently selected piece.
    '''
    def reset_squares(self, surface):
        for i in range(8):
            for j in range(0, 800, 200):
                if i % 2 == 1:
                    surface.fill((0, 0, 0), rect=(j, 100 * i, 100, 100))
                else:
                    surface.fill((0, 0, 0), rect=(j + 100, 100 * i, 100, 100))

    '''
    This function is called whenever a new game is started. Its responsibility
    is to initialize the board array by setting the correct indices to either
    CPU or USER piece objects based on how a real Checkers game starts.
    '''
    def initialize_game(self):
        board_arr = [[None for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(0, 8, 2):
                if i < 3:
                    if i % 2 == 0:
                        board_arr[i][j + 1] = Piece('CPU', i, j + 1)
                    else:
                        board_arr[i][j] = Piece('CPU', i, j)
                elif i > 4:
                    if i % 2 == 0:
                        board_arr[i][j + 1] = Piece('USER', i, j + 1)
                    else:
                        board_arr[i][j] = Piece('USER', i, j)
        self.board = board_arr

    '''
    This function returns the element at the specified row and column of the
    board array. If a piece does not exist at the given indices, this function
    will return None.
    '''
    def get_board_val(self, row, col):
        return self.board[row][col]

    '''
    This function returns true if the specified indices, i and j correspond to
    a position that exists within the boundaries of the Checkers board.
    '''
    def in_bounds(self, i, j):
        return i < 8 and j < 8 and i > -1 and j > -1

    '''
    This function takes in indices i and j and returns a boolean describing
    wether or not a position is valid for a piece to move to. That is, the
    new position must exist within the boundaries of the Checkers board and
    not be occupied by another piece.
    '''
    def valid_pos(self, i, j):
        return self.in_bounds(i, j) and self.board[i][j] is None

    '''
    This function returns a list of tuples of the form
    ((row, col), True/False). It will be called when a piece is clicked on or
    the CPU is considering a piece's moves and its purpose is to return all of
    the available spaces that the currently selected piece is allowed to move
    to. Moreover, the value True in the tuple indicates that the move is a jump
    whereas False indicates that there is no jump. This method considers the
    type of the piece selected (CPU, USER, CPU_KING, USER_KING) and checks all
    of the adjacent diagonal spaces that are valid given a piece's type. It
    also leverages the helper functions get_board_val, in_bounds, and
    valid_pos to help determine whether or not a particular space should be
    returned in the spaces available list. Note that kings must check all
    4 diagonal directions whereas non-kings only need to check 2.
    '''
    def space_available(self, piece):
        available_positions = []
        row = piece.get_row()
        col = piece.get_col()
        piece_type = piece.get_type()
        if piece_type == 'CPU':
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            if (self.in_bounds(row + 1, col - 1) and
                    self.board[row + 1][col - 1] is not None):
                if ((self.board[row + 1][col - 1].get_type() == 'USER' or
                    self.board[row + 1][col - 1].get_type() == 'USER_KING') and
                        self.valid_pos(row + 2, col - 2)):
                    available_positions.append(((row + 2, col - 2), True))
            if (self.in_bounds(row + 1, col + 1) and
                    self.board[row + 1][col + 1] is not None):
                if ((self.board[row + 1][col + 1].get_type() == 'USER' or
                    self.board[row + 1][col + 1].get_type() == 'USER_KING') and
                        self.valid_pos(row + 2, col + 2)):
                    available_positions.append(((row + 2, col + 2), True))
        elif piece_type == 'USER':
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            if (self.in_bounds(row - 1, col - 1) and
                    self.board[row - 1][col - 1] is not None):
                if ((self.board[row - 1][col - 1].get_type() == 'CPU' or
                    self.board[row - 1][col - 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row - 2, col - 2)):
                    available_positions.append(((row - 2, col - 2), True))
            if (self.in_bounds(row - 1, col + 1) and
                    self.board[row - 1][col + 1] is not None):
                if ((self.board[row - 1][col + 1].get_type() == 'CPU' or
                    self.board[row - 1][col + 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row - 2, col + 2)):
                    available_positions.append(((row - 2, col + 2), True))
        elif piece_type == 'CPU_KING':
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            if (self.in_bounds(row + 1, col - 1) and
                    self.board[row + 1][col - 1] is not None):
                if ((self.board[row + 1][col - 1].get_type() == 'USER' or
                    self.board[row + 1][col - 1].get_type() == 'USER_KING') and
                        self.valid_pos(row + 2, col - 2)):
                    available_positions.append(((row + 2, col - 2), True))
            if (self.in_bounds(row + 1, col + 1) and
                    self.board[row + 1][col + 1] is not None):
                if ((self.board[row + 1][col + 1].get_type() == 'USER' or
                    self.board[row + 1][col + 1].get_type() == 'USER_KING') and
                        self.valid_pos(row + 2, col + 2)):
                    available_positions.append(((row + 2, col + 2), True))
            if (self.in_bounds(row - 1, col - 1) and
                    self.board[row - 1][col - 1] is not None):
                if ((self.board[row - 1][col - 1].get_type() == 'USER' or
                    self.board[row - 1][col - 1].get_type() == 'USER_KING') and
                        self.valid_pos(row - 2, col - 2)):
                    available_positions.append(((row - 2, col - 2), True))
            if (self.in_bounds(row - 1, col + 1) and
                    self.board[row - 1][col + 1] is not None):
                if ((self.board[row - 1][col + 1].get_type() == 'USER' or
                    self.board[row - 1][col + 1].get_type() == 'USER_KING') and
                        self.valid_pos(row - 2, col + 2)):
                    available_positions.append(((row - 2, col + 2), True))
        elif piece_type == 'USER_KING':
            if self.valid_pos(row + 1, col - 1):
                available_positions.append(((row + 1, col - 1), False))
            if self.valid_pos(row + 1, col + 1):
                available_positions.append(((row + 1, col + 1), False))
            if self.valid_pos(row - 1, col - 1):
                available_positions.append(((row - 1, col - 1), False))
            if self.valid_pos(row - 1, col + 1):
                available_positions.append(((row - 1, col + 1), False))
            if (self.in_bounds(row + 1, col - 1) and
                    self.board[row + 1][col - 1] is not None):
                if ((self.board[row + 1][col - 1].get_type() == 'CPU' or
                    self.board[row + 1][col - 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row + 2, col - 2)):
                    available_positions.append(((row + 2, col - 2), True))
            if (self.in_bounds(row + 1, col + 1) and
                    self.board[row + 1][col + 1] is not None):
                if ((self.board[row + 1][col + 1].get_type() == 'CPU' or
                    self.board[row + 1][col + 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row + 2, col + 2)):
                    available_positions.append(((row + 2, col + 2), True))
            if (self.in_bounds(row - 1, col - 1) and
                    self.board[row - 1][col - 1] is not None):
                if ((self.board[row - 1][col - 1].get_type() == 'CPU' or
                    self.board[row - 1][col - 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row - 2, col - 2)):
                    available_positions.append(((row - 2, col - 2), True))
            if (self.in_bounds(row - 1, col + 1) and
                    self.board[row - 1][col + 1] is not None):
                if ((self.board[row - 1][col + 1].get_type() == 'CPU' or
                    self.board[row - 1][col + 1].get_type() == 'CPU_KING') and
                        self.valid_pos(row - 2, col + 2)):
                    available_positions.append(((row - 2, col + 2), True))
        return available_positions

    '''
    This function is used by the CPU to calculate a score given a particular
    piece and a move for that piece. In this version, the CPU prioritizes
    turning a piece into a king and then jumping.
    '''
    def get_move_score(self, piece, move):
        old_row = piece.get_row()
        old_col = piece.get_col()
        new_row = move[0]
        new_col = move[1]
        score = 0
        if piece.get_type() == 'CPU' and new_row == 7:
            score += 2
        delta_x = new_row - old_row
        delta_y = new_col - old_col
        if delta_x % 2 == 0 and delta_y % 2 == 0:
            score += 1
        return score

    '''
    The purpose of this function is to determine an optimal next move for the
    CPU. This is done by looping through each of the CPU's pieces, calling
    the space_available method to determine where each can move, and assigning
    scores with get_move_score. The function then considers all of the moves
    with the maximum score. If there is more then one move with the highest
    score, then a random one is chosen.
    '''
    def cpu_next_move(self):
        d = {}
        scores = []
        for i in range(8):
            for j in range(8):
                if self.get_board_val(i, j) is not None and \
                    (self.get_board_val(i, j).get_type() == 'CPU' or
                        self.get_board_val(i, j).get_type() == 'CPU_KING'):
                    p = self.get_board_val(i, j)
                    pos = (i, j)
                    if len(self.space_available(p)) != 0:
                        spaces = self.space_available(p)
                        for space in spaces:
                            scores.append(self.get_move_score(p, space[0]))
                            temp_d = {space: self.get_move_score(p, space[0])}
                            d.update({pos: temp_d})
        max_score = max(scores)
        max_score_moves = []
        for i in list(d.keys()):
            for j in list(d.get(i).keys()):
                if d.get(i).get(j) == max_score:
                    max_score_moves.append((i, j[0]))

        n = len(max_score_moves)
        random_index = randrange(n)
        move = max_score_moves[random_index]

        old_row = move[0][0]
        old_col = move[0][1]

        new_row = move[1][0]
        new_col = move[1][1]

        return old_row, old_col, new_row, new_col

    '''
    After each move is made, the update_board function is called to alter the
    board array based on where each piece is. This function also decrements
    the number of user or CPU pieces if a jump occurs and sets jumped pieces
    to None to erase them from the game. This function plays a critical role
    in redrawing the board to display the current game state.
    '''
    def update_board(self, old_row, old_col, new_row, new_col):
        board = self.board
        piece = board[old_row][old_col]
        delta_x = new_row - old_row
        delta_y = new_col - old_col
        all_moves = self.space_available(piece)
        if (new_row, new_col) in [move[0] for move in all_moves]:
            if (delta_x % 2 == 0):
                jumped_x = delta_x // 2
                jumped_y = delta_y // 2
                if (jumped_y == -1 and jumped_x == 1) or \
                        (jumped_y == 1 and jumped_x == -1):
                    board[old_row - jumped_y][old_col - jumped_x] = None
                else:
                    board[old_row + jumped_y][old_col + jumped_x] = None
                if piece.get_type() == 'USER' or \
                   piece.get_type() == 'USER_KING':
                    self.num_cpu_pieces -= 1
                else:
                    self.num_user_pieces -= 1
            board[old_row][old_col] = None
            piece.set_location(new_row, new_col)

            if piece.get_type() == 'USER' and new_row == 0:
                piece = Piece('USER_KING', new_row, new_col)
            elif piece.get_type() == 'CPU' and new_row == 7:
                piece = Piece('CPU_KING', new_row, new_col)
            board[new_row][new_col] = piece
        return board

    '''
    This function checks if the game is over by checking if there are either
    no more user or no more cpu pieces. If the number of user pieces is 0,
    then the CPU is set as the winner and vice versa.
    '''
    def check_game_over(self):
        if self.num_user_pieces == 0:
            self.winner = 'CPU'
        elif self.num_cpu_pieces == 0:
            self.winner = 'USER'
        return self.winner
