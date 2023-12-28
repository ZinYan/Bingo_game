import random


class Player:
    # Initialize Player objects
    def __init__(self, name):
        self.name = name
        self.cnt = 0
        self.board = []

    def __str__(self) -> str:
        """
        Return the Player object as a string representation (name)
        """
        return f'{self.name}'


class Game:
    # Initialize Game objects
    def __init__(self):
        self.players = []  # Player list
        self.my_player = None  # User name
        # Create 3 initial players
        self.players.append(Player('Yoo'))
        self.players.append(Player('Song'))
        self.players.append(Player('Jeon'))
        # Create number deck(1 to 9)
        self.deck = [i for i in range(1, 10)]

    def start_game(self):
        """
        Initialize each player's board and game order before the game start.
        """
        print('=============================')
        print('     Bingo Game Start!!     ')
        print('=============================')

        # Set user's name
        name = input('Enter your name(ex. Tiffany)')
        self.my_player = name
        self.players.append(Player(name))

        # Display name & board of each player
        for player in self.players:
            # name will be displayed due overloaded __str__ method
            print(f"Player's name: {player}")
            # shuffle the number deck
            random_deck = self.deck.copy()
            random.shuffle(random_deck)
            # set & display player's board
            player.board = random_deck
            self.display_board(random_deck)

        # Display Game Order
        print('=============================')
        print('         Game Order         ')
        print('=============================')
        # shuffle players list
        random.shuffle(self.players)
        # print the shuffled players
        print(
            f'Game will proceed in this order: {self.players[0]}, {self.players[1]}, {self.players[2]}, {self.players[3]}')

    def set_next_player(self, round_num):
        """
        Return the player obj for the given round number.
        """
        '''
        There are four players but there can be more than 4 rounds
        1 2 3 4     5 6 7 8     9 10 11 12 - round
        0 1 2 3(-1) 0 1 2 3(-1) 0 1  2  3(-1) - player_index
        player_index = round % 4 - 1
        4 -> number of players
        '''
        player_index = (round_num % len(self.players))-1
        return self.players[player_index]

    def count_bingo(self):
        '''
        Count bingos for each player
        '''
        for player in self.players:
            # Changing board to 2d matrix (from [1,2,3,4,5,6,7,8,9] to [[1,2,3],[4,5,6],[7,8,9]])
            board = []
            for i in range(0, len(player.board), 3):
                board.append(player.board[i:i+3])

            # Initializes the number of bingo in the player as this process will be done for every round
            player.cnt = 0

            # Counting zeros
            # all() -> return True if all elements in the iterable is True
            '''
            board = [[1,0,3],[0,0,0],[0,3,5]]
            output = ((num==0 for num in row) for row in board) #((False,True,False),(True,True,True),(True,False,False))
            # doing this is equal to (all(False,True,False),all(True,True,True),all(True,False,False))
            output = (all(num==0 for num in row) for row in board) # False True False
            output = sum((all(num==0 for num in row) for row in board)) #1 (False=0, True=1)
            '''
            # counting number of of all zero row
            player.cnt += sum(all(num == 0 for num in row)
                              for row in board)
            # counting number of all zero column
            player.cnt += sum(all(row[col_index] == 0 for row in board)
                              for col_index in range(len(board[0])))
            # counting number of all zero diagonals
            # Main diagonal - matrix[0][0], matrix[1][1], matrix[2][2]
            player.cnt += all(board[i]
                              [i] == 0 for i in range(len(board)))
            # Sub-diagonal - matrix[0][2], matrix[1][1], matrix[2][0]
            player.cnt += all(board[i]
                              [len(board)-1-i] == 0 for i in range(len(board)))

    def display_board(self, player_deck):
        '''
        Display bingo board in chunks(3x3)
        [5, 1, 4, 7, 8, 9, 2, 3, 6] ->
        [5, 1, 4]
        [7, 8, 9]
        [2, 3, 6]
        '''
        print("===Player's Table===")
        for i in range(0, len(player_deck), 3):
            # 1st loop - 0 to 2 / 2nd - 3 to 5 / 3rd - 6 to 8
            chunk = player_deck[i:i+3]
            print(chunk)

    def do_bingo(self, chosen_num):
        '''
        Change chosen number to zero and display information of each player.
        '''
        print(f'chosen num: {chosen_num}')
        for player in self.players:
            # change chosen number to zero in the board
            player.board = [num if num !=
                            chosen_num else 0 for num in player.board]
            # count bingos for each player
            self.count_bingo()
            print(f'>> {player} (Current Bingo: {player.cnt})')
            # display the bingo board
            self.display_board(player.board)

    def play_game(self):
        '''
        Play bingo game until there is someone with 3 bingos.
        '''
        round_num = 0
        while True:
            # Start round
            round_num += 1
            print(' =============================')
            print(f'      ROUND {round_num} - START       ')
            print(' =============================')

            # Set the player of this round
            next_player = self.set_next_player(round_num)
            # will print name of player_obj due to __str__ method.
            print(f"It's {next_player} turn. ")

            # Choose number
            # remove zero from the board to display it to players
            non_zero_board = [num for num in next_player.board if num != 0]
            # if this round player(next_player) is a user -> get numeric input from the user among unchosen numbers
            # if this round player(next_player) is other players -> choose random number among unchosen numbers
            if next_player.name == self.my_player:
                while True:  # Exception Handling
                    try:
                        num = int(input(
                            f"It's your turn. Choose one among unchosen numbers. Unchosen Numbers: {sorted(non_zero_board)}"))
                        if num in non_zero_board:
                            break
                        elif num > 9 or num < 0:
                            print(
                                "It's outside of the range. Please choose a number within the range(0~9) among unchosen numbers.")
                            continue
                        elif num not in non_zero_board:
                            print(
                                "It's already chosen number. Please choose a number among unchosen ones.")
                    except ValueError:
                        print(
                            "It's not an integer. Please choose a number within the range(0~9) among unchosen numbers ")
                    except Exception as e:
                        print(e)
            else:
                num = random.choice(non_zero_board)
            # print chosen number
            print(f'{next_player} choose {num}.')

            # Do bingo (change chosen num to zero & display information of each player)
            self.do_bingo(num)

            # Print round end
            print('=============================')
            print(f'      ROUND {round_num} - END       ')
            print('=============================')
            # If any of the players have achieved greater than or equal 3 bingo, the function will be terminated.
            for player in self.players:
                if player.cnt >= 3:
                    return
            print()

    def game_result(self):
        '''
        Display the result of the game
        '''
        print('=============================')
        print('     Rank - Bingo Count      ')
        print('=============================')

        # Notes for determining rank according to bingo count
        # Even if repetition exit, there will be two person with same rank.
        # The rank after repetitive rank will be the consecutive rank of that.
        # e.g., 1st-'Yoo', 1st-'Song', 1st-Jeon', 2nd-'Tiffany'

        # Create a dict(player_cnt) with keys:count(8,7,6,5,4,3,2,1,0 -> 8 possible bingo counts) and values:players_list(empty lists)
        # {8: [], 7: [], 6: [], 5: [], 4: [], 3: [], 2: [], 1: [], 0: []}
        player_cnt = {key: [] for key in [i for i in range(8, -1, -1)]}

        # Add players to the dictionary according to their counts
        # {3:['Yoo','Song', 'Jeon'], 2:[], 1:['Tiffany'], 0:[]}
        # [player_lst.append(player) for player in self.players for cnt,player_lst in player_cnt.items() if cnt == player.cnt]
        for player in self.players:
            for cnt, player_lst in player_cnt.items():
                if cnt == player.cnt:
                    player_lst.append(player)

        # Print rank, name, bingo count
        rank = 0
        for cnt, player_lst in player_cnt.items():
            # if there is a player in that count, rank will be increased.
            if player_lst != []:
                rank += 1
            # print every player with same bingo count as the same rank
            # my_player -> *name*, others -> name
            for player in player_lst:
                name = f"*{player}*" if player.name == self.my_player else player
                print(f'{rank} - {name} : Bingo Count {player.cnt}')

    def game(self):
        '''
        Run the game.
        '''
        self.start_game()
        self.play_game()
        self.game_result()


if __name__ == "__main__":
    ''' Create game object and run the codes. '''
    game = Game()
    game.game()
