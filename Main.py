__author__ = 'taylor'

import copy
import time
from tkinter import *

def game_loop(width, height, initial_board_state):
    """
    Main game loop setups initial board state from input.
    width : int
        Integer representing the length of the X axis of the board
    height : int
        Integer representing the length of the Y axis of the board
    initial_state : list(list())
        List of tuples of 0 and 1 that will populate the initial board from
        bottom up. The state will populate as much as possible from the tuples
        and assume anything not specified is a dead cell(zero).
    """
    tk = Tk()

    # Setup initial state
    current_board = Board(tk, width, height)
    current_board.set_state(initial_board_state)
    time.sleep(2000)
    current_board.advance_board_state()
    tk.mainloop()


class Board(object):
    """
    Board holds the current state of the game and can advance the state to the
    next state.
    """
    def __init__(self, tk_obj, width=2, height=2):
        self.tk = tk_obj
        self.window = Canvas(tk_obj, width=800, height=600)
        self.window.pack()
        self.width = width
        self.height = height
        self.board = [[0 for _x in range(width)] for _y in range(height)]

    def set_state(self, board_state):
        for row_id, row in enumerate(board_state):
            for col_id, cell in enumerate(row):
                if cell in (0, 1):
                    try:
                        self.board[row_id][col_id] = cell
                    except IndexError:
                        continue
                else:
                    raise TypeError
        self.print_board(self.window)

    def advance_state(self):
        next_state = list()
        for row_id, row in enumerate(self.board):
            new_row = row.copy()
            for col_id, cell in enumerate(row):
                current_cell = self.board[row_id][col_id]
                neighbor_count = self.check_cell_neighbors(row_id, col_id)
                if current_cell == 1:
                    if neighbor_count < 2:
                        new_row[col_id] = 0  # RIP lonely fellow
                    elif neighbor_count in (2, 3):
                        # Teamwork makes the dream work
                        new_row[col_id] = 1
                    elif neighbor_count > 3:  # RIP agoraphobia
                        new_row[col_id] = 0
                else:
                    if neighbor_count == 3:
                        new_row[col_id] = 1  # The miracle of life!
                    else:
                        new_row[col_id] = 0  # You may or may not be remembered
            next_state.append(new_row)
        self.set_state(next_state)

    def check_cell_neighbors(self, row_id, col_id):
        neigh_count = int()
        neighbors = [(-1, 1),
                     (0, 1),
                     (1, 1),
                     (-1, 0),
                     (1, 0),
                     (-1, -1),
                     (0, -1),
                     (1, -1)]
        for adj in neighbors:
            x_adj = row_id + adj[0]
            y_adj = col_id + adj[1]
            try:
                neigh_count += self.get_cell_status(x_adj, y_adj)
            except TypeError:
                # get_cell_status returned None which means the neighbor was
                # out of bounds
                continue

        return neigh_count

    def get_cell_status(self, row_id, col_id):
        try:
            if self.board[row_id][col_id] == 1:
                return 1
            else:
                return 0
        except IndexError:
            return None

    def print_board(self, window):
        output_board = copy.deepcopy(self.board)
        cell_height = window.winfo_height() / self.height
        cell_width = window.winfo_width() / self.width
        for row_id, row in enumerate(output_board):
            for col_id, cell in enumerate(row):
                cell_x1 = cell_width * col_id
                cell_y1 = cell_height * row_id
                cell_x2 = cell_x1 + cell_width
                cell_y2 = cell_y1 + cell_height
                curr_cell = output_board[row_id][col_id]
                if curr_cell == 1:
                    window.create_rectangle(cell_x1,
                                            cell_y1,
                                            cell_x2,
                                            cell_y2,
                                            fill='black')
                else:
                    window.create_rectangle(cell_x1,
                                            cell_y1,
                                            cell_x2,
                                            cell_y2,
                                            fill='white')

    def advance_board_state(self):
        self.advance_state()
        self.tk.after(2000, self.advance_board_state)

if __name__ == '__main__':
    initial_state = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    game_loop(10, 10, initial_state)