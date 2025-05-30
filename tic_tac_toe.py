import tkinter as tk
from tkinter import font
from players import Move
from game import TicTacToeGame

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title('Tic-Tac_Toe Game🔥☑️')
        self.attributes("-fullscreen", True)
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_display_board()
        self._create_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        file_menu.add_cascade(label="File", menu=menu_bar)

    def _create_display_board(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text='Ready?',
            font=font.Font(size=28, weight='bold')
        )
        self.display.pack()

    def _create_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()

        for row in range(self._game.board_size):
            self.rowconfigure(row, minsize=50, weight=1)
            self.columnconfigure(row, minsize=75, weight=1)

            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text='',
                    font=font.Font(weight='bold', size=30),
                    fg="black",
                    height=2,
                    width=6,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=6,
                    sticky="nsew"
                )

    def play(self, event):
        """Handle a player's move"""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)

        if self._game._is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)

            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")

            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)

            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                color = self._game.current_player.color
                self._update_display(msg, color)



    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)


    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color


    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    game_board = TicTacToeBoard(game)
    game_board.mainloop()


if __name__ == "__main__":
    main()