import copy

class node():
    def __init__(self, state, previous_node, previous_action):
        self.state = state
        self.parent = previous_node
        self.previous_action = previous_action
    

class pentago():
    def __init__(self):
        self.board = [[' ']*6 for _ in range(6)]
        self.player = 'o'
        self.lines_h = [[(i,j+k) for k in range(5)] 
                        for i in range(6) for j in range(2)]
        self.lines_v = [[(i+k,j) for k in range(5)]
                        for i in range(2) for j in range(6)]
        self.lines_d1 = [[(i+k,j+k) for k in range(5)] 
                         for i in range(2) for j in range(2)]
        self.lines_d2 = [[(i+k,j-k) for k in range(5)] 
                         for i in range(2) for j in range(4,6)]
        self.lines = self.lines_h+self.lines_v+self.lines_d1+self.lines_d2
    
    def print_board(self):
        for i in range(11):
            for j in range(11):
                if i % 2 == 1:
                    print('-', end = '')
                elif j % 2 == 1:
                    print('|', end = '')
                else:
                    print(self.board[int(i/2)][int(j/2)], end = '')
            print('')
        print('\n')
        
    
    def replace_board(self, board):
        # for testing purposes
        self.board = board
    
    def moves(self):
        moves = [(i,j,quadrant, direction)
                 for i in range(6)
                 for j in range(6)
                 if self.board[i][j] == ' '
                 for quadrant in range(4)
                 for direction in ['c', 'ac']]
        return moves
    
    def ask_for_move(self):
        move = input('Please enter your move: ')
        i,j,q,d = move.split(',')
        i,j,q = int(i), int(j), int(q)
        return (i,j,q,d)
    
    def rotate(self, quadrant, direction):
        q = [[0,0], [0,1], [1,0], [1,1]][quadrant]
        temp = copy.deepcopy(self.board)
        sub_board = [ [temp[3*q[0]+i][3*q[1]+j]
                       for j in range(3)] for i in range(3)]
        
        if direction == 'c':
            for i in range(3):
                for j in range(3):
                    self.board[3*q[0]+i][3*q[1]+j] = sub_board[2-j][i]
                    
        if direction == 'ac':
            for i in range(3):
                for j in range(3):
                    self.board[3*q[0]+i][3*q[1]+j] = sub_board[j][2-i]
    
    def update_board(self, move):
        i,j, quadrant, direction = move
        self.board[i][j] = self.player
        self.rotate(quadrant, direction)
        
        if self.player == 'o':
            self.player = 'x'
        else:
            self.player = 'o'
    
    def play(self):
        while not(self.game_over()):
            self.print_board()
            print(f'Current player is: {self.player} \n')
            move = self.ask_for_move()
            print('')
            self.update_board(move)
            self.game_over()
        
        print('The game has ended')
        self.print_board()
        if self.value == 1:
            print('The winner is o')
        elif self.value == 0:
            print('The winner is x')
        elif self.value == 0.5:
            print('It is a draw')
    
    def game_over(self):
        if any(
                [ all(
                    [self.board[i][j] == 'o'
                     for i,j in line ]
                    )
                 for line in self.lines]):
            self.value = 1
            return True
        elif any(
                [ all(
                    [self.board[i][j] == 'x'
                     for i,j in line ]
                    )
                 for line in self.lines]):
            self.value = 1
            return True
        elif len(self.moves()) == 0:
            self.value = 0.5
            return True
        return False






# board = [[' ']*6 for _ in range(6)]

# board1 = [[' ', ' ', ' ', ' ', ' ', ' '],
#           [' ', ' ', ' ', ' ', ' ', ' '],
#           [' ', ' ', ' ', ' ', ' ', ' '],
#           [' ', ' ', ' ', ' ', ' ', ' '],
#           [' ', ' ', ' ', ' ', ' ', ' '],
#           [' ', ' ', ' ', ' ', ' ', ' ']
#     ]

board2 = [['o', 'o', 'o', 'x', 'x', 'x'],
          ['x', 'x', 'x', 'o', 'o', 'o'],
          ['o', 'o', 'o', 'x', 'x', 'x'],
          ['x', 'x', 'x', 'o', 'o', 'o'],
          ['o', 'o', 'o', 'x', 'x', 'x'],
          ['x', 'x', 'x', 'o', 'o', ' ']
    ]

board3 = [['o', 'x', 'x', 'o', 'x', 'o'],
          ['o', ' ', ' ', ' ', ' ', ' '],
          ['o', 'o', 'o', 'o', 'x', 'x'],
          [' ', ' ', ' ', ' ', ' ', ' '],
          ['x', 'x', 'x', 'o', 'o', 'o'],
          [' ', 'o', ' ', ' ', 'x', ' ']
    ]


test = pentago()
test.replace_board(board2)
test.play()



# test.replace_board(board3)
# test.print_board()
# test.update_board((1,4,1,'c'))
# test.print_board()

# test.rotate(0,'ac')
# test.print_board()
# print(test.player)


# testing set of lines is correct
# test = pentago()
# for line in lines:
#     new_board = copy.deepcopy(board)
#     for i,j in line:
#         new_board[i][j] = 'o'
#         test.replace_board(new_board)
#     test.print_board()