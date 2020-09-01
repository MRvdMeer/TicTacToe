import tkinter as tk


class Game(tk.Frame):

    def __init__(self, master):
        super(Game, self).__init__(master)
        self.width = 800
        self.height = 800
        self.canvas = tk.Canvas(self, bg='#aabbff', width=self.width, height=self.height)
        self.draw_board()
        self.canvas.pack()
        self.pack()
        self.pieces = []
        self.add_piece(1, 1, 1)

    def draw_board(self):
        x_pos = [(self.width / 3) * i for i in [1, 2]]
        y_pos = [(self.height / 3) * i for i in [1, 2]]

        for x in x_pos:
            self.canvas.create_line(x, 0, x, self.height, width=2.0, fill='black')

        for y in y_pos:
            self.canvas.create_line(0, y, self.width, y, width=2.0, fill='black')

    def add_piece(self, player, x_loc, y_loc):
        piece = PlayerPiece(self.canvas, player, x_loc, y_loc)
        self.pieces.append(piece)


class GameObject:
    def __init__(self, canvas, item, x_loc, y_loc):
        self.canvas = canvas
        self.item = item
        self.x_loc = x_loc
        self.y_loc = y_loc

    def get_position(self):
        return self.x_loc, self.y_loc

    def delete(self):
        self.canvas.delete(self.item)


class PlayerPiece(GameObject):
    """
    player is the player who places the piece (0 or 1)
    x_loc is the x location of the piece (0, 1, 2)
    y_loc is the y location of the piece (0, 1, 2)
    """

    def __init__(self, canvas, player, x_loc, y_loc):
        square_height = canvas.winfo_height() / 3
        square_width = canvas.winfo_width() / 3
        self.height = square_height * 0.8
        self.width = square_width * 0.8

        if player == 0:
            item = 1
            # player 1 plays 'X'

            #item = canvas.create_line()
        elif player == 1:
            # player 2 plays 'O'
            item = canvas.create_oval((x_loc + 0.1) * square_width,
                                      (y_loc + 0.1) * square_height,
                                      (x_loc + 0.9) * square_width,
                                      (y_loc + 0.9) * square_height,
                                      fill='white')
        else:
            raise ValueError('player must be 0 or 1')

        super(PlayerPiece, self).__init__(canvas, item, x_loc, y_loc)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TicTacToe!')
    game = Game(root)
    game.mainloop()

