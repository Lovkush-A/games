import copy
    

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
        # manually change the board, for testing purposes
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
        if any([
                all([
                    self.board[i][j] == 'o' for i,j in line
                    ])
                for line in self.lines
                ]):
            self.value = 1
            return True
        elif any([
                all([
                    self.board[i][j] == 'x' for i,j in line
                    ])
                for line in self.lines
                ]):
            self.value = 0
            return True
        elif len(self.moves()) == 0:
            self.value = 0.5
            return True
        return False


class Node():
    def __init__(self, board, player, parent, action, depth):
        self.board = board
        self.player = player
        self.parent = parent
        self.action = action
        self.depth = depth
        self.max_value = 1
        self.min_value = 0
        self.valueless_children = 0
        self.value = None
        self.best_move = None


class Frontier():
    def __init__(self):
        self.nodes = []
        self.boards = []
    
    def next_node(self):
        node = self.nodes[-1]
        self.nodes = self.nodes[:-1]
        return node
    
    def add_node(self, node):
        self.nodes.append(node)
        self.boards.append([node.parent, node.board])


def find_move(board, player, max_depth):
    
    initial_node = Node(board, player, None, None, depth=0)
    frontier = Frontier()
    frontier.add_node(initial_node)
    
    while initial_node.value is None:
        current_node = frontier.next_node()
        current_board = current_node.board
        
        # if current_node.depth == 2:
        #     x,y,*c = current_node.action
        #     if current_node.action == (1,3,1,'c'):
        #         x = x
        
        if game_over(current_board, lines) is not None:
            current_node.value = game_over(current_board, lines)
            update_parents(current_node)
        elif current_node.depth == max_depth:
            current_node.value = 0.5
            update_parents(current_node)
        else:
            for move in moves(current_board):        
                new_board_ = new_board(current_board,
                                      current_node.player,
                                      move)
                
                if [current_node, new_board_] in frontier.boards:
                    continue
                
                new_node = Node(new_board_,
                                1 - current_node.player,
                                current_node,
                                move,
                                current_node.depth + 1)
                
                frontier.add_node(new_node)
                
                current_node.valueless_children += 1
    
    # return initial_node.value, initial_node.best_move
    return initial_node.best_move


def update_parents(node):
    parent = node.parent
    
    if parent.player == 1 and node.value > parent.min_value:
        parent.min_value = node.value
        parent.best_move = node.action
    elif parent.player == 0 and node.value < parent.max_value:
        parent.max_value = node.value
        parent.best_move = node.action
    
    parent.valueless_children -= 1
    
    # if node.depth == 1:
    #     print(parent.valueless_children)
    
    if parent.valueless_children == 0:
        if parent.player == 1:
            parent.value = parent.min_value
        elif parent.player == 0:
            parent.value = parent.max_value
            
        if parent.depth > 0:
            update_parents(parent)


def moves(board):
    moves = [(i,j,quadrant, direction)
             for i in range(6)
             for j in range(6)
             if board[i][j] == ' '
             for quadrant in range(4)
             for direction in ['c', 'ac']]
    return moves
    

def new_board(board, player, move):
    i,j, quadrant, direction = move
    new_board = copy.deepcopy(board)
    new_board[i][j] = player
    
    # create array of quadrant of original board to be rotated
    q = [[0,0], [0,1], [1,0], [1,1]][quadrant]
    temp = copy.deepcopy(new_board)
    sub_board = [ [temp[3*q[0]+i][3*q[1]+j]
                   for j in range(3)] for i in range(3)]    
    
    # rotate quadrant and update new board
    if direction == 'c':
        for i in range(3):
            for j in range(3):
                new_board[3*q[0]+i][3*q[1]+j] = sub_board[2-j][i]
                
    if direction == 'ac':
        for i in range(3):
            for j in range(3):
                new_board[3*q[0]+i][3*q[1]+j] = sub_board[j][2-i]   
    
    return new_board


def print_board(board):
    for i in range(11):
        for j in range(11):
            if i % 2 == 1:
                print('-', end = '')
            elif j % 2 == 1:
                print('|', end = '')
            else:
                print(board[int(i/2)][int(j/2)], end = '')
        print('')
    print('\n')


def create_lines():
    lines_h = [[(i,j+k) for k in range(5)] 
               for i in range(6) for j in range(2)]
    lines_v = [[(i+k,j) for k in range(5)]
               for i in range(2) for j in range(6)]
    lines_d1 = [[(i+k,j+k) for k in range(5)] 
                for i in range(2) for j in range(2)]
    lines_d2 = [[(i+k,j-k) for k in range(5)] 
                for i in range(2) for j in range(4,6)]
    return lines_h+lines_v+lines_d1+lines_d2
lines = create_lines()


def game_over(board, lines):
    if any([
            all([
                board[i][j] == 1 for i,j in line
                ])
            for line in lines
            ]):
        return 1
    elif any([
            all([
                board[i][j] == 0 for i,j in line
                ])
            for line in lines
            ]):
        return 0
    elif len(moves(board)) == 0:
        return 0.5
    return None


def ask_for_move():
    move = input('Please enter your move: ')
    i,j,q,d = move.split(',')
    i,j,q = int(i), int(j), int(q)
    return (i,j,q,d)


def play():
    board = [[' ']*6 for _ in range(6)]
    ai =  False
    player = 1
    
    while game_over(board, lines) is None:
        print('')
        print_board(board)
        print(f'Current player is: {player} \n')
        
        if ai == False:
            move = ask_for_move()
            ai = True
        elif ai == True:
            print('ai is thinking...')
            move = find_move(board, player, 2)
            if move is None:
                move = moves(board)[0]
            ai = False
            
        board = new_board(board, player, move)
        player = 1 - player
    
    print('The game has ended')
    print_board(board)
    print(f'the final score is {game_over(board, lines)}')

def test():
)    board = [[' ']*6 for _ in range(6)]
    
    
    board2 = [[1,1,1,0,0,0],
              [0,0,0,1,1,1],
              [1,1,1,0,0,0],
              [0,0,0,1,1,1],
              [1,1,1,0,0,0],
              [0,0,0,1,1,' ']]
    
    # 1 to win , and 0 cannot block
    board3 = [[1  ,0  ,0  ,1  ,0  ,1  ],
              [1  ,' ',' ',' ',' ',' '],
              [1  ,1  ,1  ,1  ,0  ,0  ],
              [' ',' ',' ',' ',' ',' '],
              [0,  0,  0,  1,  1,  1  ],
              [' ',1  ,' ',' ',0  ,' ']]
              
    
    # 0 to win immediately
    board4 = [[0,0,0,0, ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ']]
    
    # 1 to find winning move
    board5 = [[' ', ' ', ' ', ' ', ' ', ' '],
              [' ',1,1, ' ',1, ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ']]

    # print_board(board4)
    # print("Move for player 0: ", end='')
    # print(find_move(board4,0,1))
    # print("Move for player 1: ", end='')
    # print(find_move(board4,1,2))
    
    # print_board(board3)
    # print("Move for player 1: ", end='')
    # print(find_move(board3,1,1))
    # print("Move for player 0: ", end='')
    # print(find_move(board3,0,2))
    
    # print('\nWinning position if player 1 makes their move:')
    # print_board(new_board(board3, 1, find_move(board3,1,1)))    
    
    # print_board(board2)
    # print(moves(board2))
    # for move in moves(board3):
    #     print(move)
    #     new = new_board(board3, 1, move)
    #     print_board(new)
    #     print(game_over(new, lines))
    
    
    # test = pentago()
    # test.replace_board(board4)
    # test.play()
    
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
    
    return None


play()