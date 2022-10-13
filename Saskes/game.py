import pygame
import pygame.freetype
from Saskes.board import Board
from .constants import RED, WHITE, BLUE, SQUARE_SIZE

class Game:
    def __init__(self, win, boughtProducts):
        self._init()
        self.win = win
        self.boughtProducts = boughtProducts

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def update(self): # atnaujina lenta
        self.board.draw(self.win, self.boughtProducts)
        self.draw_valid_moves(self.valid_moves)
        if self.board.winner():
            self._winner(self.win)
        pygame.display.update()

    def _winner(self, win): # kai atsiranda laimetojas
        font = pygame.font.Font('freesansbold.ttf', 50)

        if self.board.winner() == WHITE:
            laimetojas = font.render("Laimejo baltasis!", True, (0, 255, 0))
        else:
            laimetojas = font.render("Laimejo rudasis!", True, (0, 255, 0))

        win.blit(laimetojas, (200, 300))

    def select(self, row, col): # paimti saske
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

    def _move(self, row, col): #padaryti judesi
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()

        else:
            return False

        return True

    def draw_valid_moves(self, moves):# nupaiso galimus judesius
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board): # kompiuteris padaro judesi
        self.board = board
        self.change_turn()
