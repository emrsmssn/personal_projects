import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.player_selected_piece = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.player_selected_piece:
            move_result = self._move(row, col)
            #if not move_result:
                #self.player_selected_piece = None
                #self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.player_selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.player_selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.player_selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()

        else:
            return False
        
        return False

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED: 
            self.turn = WHITE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def winner(self):
        return self.board.winner()
