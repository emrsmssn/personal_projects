import pygame
from .constants import BLACK, WHITE, COLS, RED, ROWS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_remaining = self.white_remaining = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_board(self, win):
        win.fill(BLACK)

        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_board(win)
        for row in range(ROWS):
            for col in range(ROWS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == 0 or row == ROWS - 1:
            piece.make_king()

            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        direction = -1 if piece.color == RED else 1
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        moves.update(self._moves_left(row+direction, left, direction, piece.color, False))
        moves.update(self._moves_right(row+direction, right, direction, piece.color, False))

        if piece.king:
            moves.update(self._moves_left(row-direction, left, -direction, piece.color, False))
            moves.update(self._moves_right(row-direction, right, -direction, piece.color, False))

        #if piece.color == RED or piece.king:
         #   moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
          #  moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        #if piece.color == WHITE or piece.king:
         #   moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
          #  moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _moves_left(self, row, col, direction, piece_color, jumping, jumped=[]):
        moves = {}
        pieces_jumped = []

        if row > 7 or row < 0 or col > 7 or col < 0:
            return moves

        square = self.get_piece(row, col)

        if square == 0 and not jumping:
            moves[(row, col)] = pieces_jumped

        elif square != 0 and square.color != piece_color:

            if row+direction > 7 or row+direction < 0 or col-1 > 7 or col-1 < 0:
                return moves    

            possible_jump = self.board[row+direction][col-1]
            if possible_jump == 0:
                pieces_jumped = [square]
                moves[(row+direction, col-1)] = pieces_jumped + jumped
                #recurse for more jumps
                moves.update(self._moves_left(row+2*direction, col-2, direction, piece_color, True, jumped=pieces_jumped))
                moves.update(self._moves_right(row+2*direction, col, direction, piece_color, True, jumped=pieces_jumped))
            else:
                pass

        i = 1
        return moves
    
    def _moves_right(self, row, col, direction, piece_color, jumping, jumped=[]):
        moves = {}
        pieces_jumped = []

        if row > 7 or row < 0 or col > 7 or col < 0:
            return moves

        square = self.get_piece(row, col)

        if square == 0 and not jumping:
            moves[(row, col)] = pieces_jumped

        elif square != 0 and square.color != piece_color:

            if row+direction > 7 or row+direction < 0 or col+1 > 7 or col+1 < 0:
                return moves

            possible_jump = self.board[row+direction][col+1]
            if possible_jump == 0:
                pieces_jumped = [square]
                moves[(row+direction, col+1)] = pieces_jumped + jumped
                #recurse for more jumps
                moves.update(self._moves_left(row+2*direction, col, direction, piece_color, True, jumped=pieces_jumped))
                moves.update(self._moves_right(row+2*direction, col+2, direction, piece_color, True, jumped=pieces_jumped))
            else:
                pass

        i = 1
        return moves      
        

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last + skipped

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last + skipped

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1     

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

            if piece.color == RED:
                self.red_remaining -= 1
            else:
                self.white_remaining -= 1
    
    def winner(self):
        if self.red_remaining <= 0:
            return WHITE
        elif self.white_remaining <= 0:
            return RED
        
        return None