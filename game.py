import os
import math
from pynput import keyboard

class Game:
    """
    A game of TicTacToe
    """

    def __init__(cls):
        cls.size = None
        cls.empty = '-'
        cls.cursor = '*'
        cls.board = []
        cls.position = 0

        # Who won or tie
        cls.winner = None

        # Whos turn is it
        cls.current_player = 'X'


    def play_game(cls):
        """
        This starts the main game loop
        """
        os.system('cls')
        # Get the board size
        prompt = "What size board do you want? (3-10)"
        size = input(prompt)
        while size not in [str(x) for x in range(3, 11)]:
            size = input(prompt)
        cls.size = int(size)

        cls.clear_board()

        # Non-blocking fashion
        listener = keyboard.Listener(on_release=cls.on_release)
        listener.start()


    def clear_board(cls):
        """
        Set the board for a new game
        """
        # Set the board dimensions
        cls.board = [[cls.empty for x in range(cls.size)] for y in range(cls.size)]
        
        # Set allowed positions the user may provide
        cls.positions = [str(x) for x in range(1, cls.size**2 + 1)]

        cls.current_player = 'X'

        cls.display_board()

        cls.prompt_player()

    def clear_screen(cls):
        try: 
            os.system('cls')
        except:
            pass
        try:
            os.system('cls')
        except:
            pass

    def display_board(cls, display_position = False):
        """
        Display the game board in the console
        """
        cls.clear_screen()

        if display_position:
            # Copy board
            copy = []
            for row in range(0, cls.size):
                set = []
                for col in range(0, cls.size):
                    set.append(str(cls.board[row][col]))
                copy.append(set)
            
            # Set the current position
            row, col = cls.get_position_coords()
            copy[row][col] = cls.cursor
            [print(' | '.join(row)) for row in copy]

            cls.prompt_player()

        else:
            [print(' | '.join(row)) for row in cls.board]


    def on_release(cls, key):
        """
        Handle keyboard input
        """
        # Handle a single turn of an arbitrary player
        cls.handle_turn(key)
    
    
    def up(cls):
        """
        Move cursor up
        """
        cls.position -= cls.size
        if cls.position < 1:
            cls.position = 0
    
    
    def down(cls):
        """
        Move cursor down
        """
        cls.position += cls.size
        if cls.position > cls.size**2 - 1:
            cls.position -= cls.size**2
    
    
    def left(cls):
        """
        Move cursor left
        """
        cls.position -= 1
        if cls.position < 1:
            cls.position = 0
    
    
    def right(cls):
        """
        Move cursor right
        """
        cls.position += 1
        if cls.position > cls.size**2 - 1:
            cls.position = cls.size**2 - 1


    def get_position_coords(cls):
        """
        Get coordinates for the current position
        """
        row = math.floor(cls.position / cls.size)
        col = cls.position - row * cls.size
        return row, col


    def handle_turn(cls, key):
        """
        Handle input to choose the position
        """
        entered = str(key).replace("'", "")

        if entered in ['a','s','d','w']:
            switcher = {
                'w': cls.up,
                's': cls.down,
                'a': cls.left,
                'd': cls.right,
            }
            switcher.get(entered)()
            cls.display_board(True)
        
        elif entered in cls.positions:
            cls.position = int(entered) - 1

        elif entered == 'Key.enter':
            row, col = cls.get_position_coords()
            if cls.board[row][col] == cls.empty:
                # Board will place an X or O on the number slot chosen
                cls.board[row][col] = cls.current_player

                # Check if the game has ended
                cls.is_game_over()

                # Flip to other player
                cls.flip_player()

                # Declare winner and clear board
                if(cls.winner):
                    print(f'{cls.winner} wins!')
                    input('Press enter to play again.')
                    cls.clear_board()
            else:
                print("You can't go there. Asshole.")


    def is_game_over(cls):
        """
        Determine if game is over
        """
        cls.record_winner()
        cls.record_tie()


    def record_winner(cls):
        """
        Determine if there is a winner and set the winner
        """
        # Determine number of contiguous positions needed to win
        win_length = 3 if cls.size == 3 else 4

        # Store all sets of coordinates for contiguous positions
        sets = []

        # Loop through all 3x3 squares on the board
        for x in range(0, cls.size-(win_length-1)):
            for y in range(0, cls.size-(win_length-1)):
                # Add sets for rows
                for row in range(x, x+win_length):
                    set = []
                    for col in range(y, y+win_length):
                        set.append([row, col])
                    sets.append(set)
                # Add sets for columns
                for col in range(y, y+win_length):
                    set = []
                    for row in range(x, x+win_length):
                        set.append([row, col])
                    sets.append(set)
                # Add sets for diagonals
                if cls.size == 3:
                    sets.append([[x,y],[x+1,y+1],[x+2,y+2]])
                    sets.append([[x,y+2],[x+1,y+1],[x+2,y]])
                else:
                    sets.append([[x,y],[x+1,y+1],[x+2,y+2],[x+3,y+3]])
                    sets.append([[x,y+3],[x+1,y+2],[x+2,y+1],[x+3,y]])

        # Check all sets for winner
        for set in sets:
            d = {}
            for coords in set:
                token = cls.board[coords[0]][coords[1]]
                d[token] = token != cls.empty
            # If the dictionary only has one key and it's not empty, then we have a winner
            tokens = list(d.keys())
            if len(tokens) == 1 and d[tokens[0]]:
                cls.winner = tokens[0]


    def record_tie(cls):
        """
        Check for tie game and set the winner
        """
        d = {}
        for row in range(0, cls.size):
            for col in range(0, cls.size):
                token = cls.board[row][col]
                d[token] = token
        if cls.winner is None and cls.empty not in list(d.keys()):
            cls.winner = 'Tie'


    def flip_player(cls):
        """
        Flip player from X to O and back
        """
        cls.current_player = 'X' if cls.current_player == 'O' else 'O'

        cls.display_board()
        cls.prompt_player()
        
    
    def prompt_player(cls):
        # Prompt player
        print(cls.current_player + "'s turn.")

