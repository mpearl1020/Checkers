import pygame
from PIL import Image

'''
Loads the piece images for USER, USER_KING, CPU, CPU_KING and stores them
in a dictionary that maps a string representing the type of the piece to
its image
'''
cp = Image.open('cpu_piece.PNG')
cpu_piece_pic = pygame.image.fromstring(cp.tobytes(), cp.size, cp.mode)
ck = Image.open('cpu_king.PNG')
cpu_king_piece_pic = pygame.image.fromstring(ck.tobytes(), ck.size, ck.mode)
up = Image.open('user_piece.PNG')
user_piece_pic = pygame.image.fromstring(up.tobytes(), up.size, up.mode)
uk = Image.open('user_king.PNG')
user_king_piece_pic = pygame.image.fromstring(uk.tobytes(), uk.size, uk.mode)

icon_dict = {'CPU': cpu_piece_pic, 'CPU_KING': cpu_king_piece_pic,
             'USER': user_piece_pic, 'USER_KING': user_king_piece_pic}

'''
The Piece class allows USER, USER_KING, CPU, and CPU_KING objects to be
instantiated. It contains information about whether or not the piece is a
king, the type of the piece, its current position (defined by a row and column
in the checker board) and an image icon.
'''


class Piece:
    '''
    Constructor for the instance variables descibed above
    '''
    def __init__(self, type, row, col):
        self.is_king = False
        self.type = type
        self.row = row
        self.col = col
        self.icon = icon_dict.get(type)

    '''
    Allows objects of type Piece to be compared
    '''
    def __eq__(self, other_piece):
        return self.__dict__ == other_piece.__dict__

    '''
    The following functions are accessor methods for the piece's icon, current
    row and column, and its type.
    '''
    def get_icon(self):
        return self.icon

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_type(self):
        return self.type

    '''
    This function allows a piece to be assigned a new position defined by
    a new row and new column.
    '''
    def set_location(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
