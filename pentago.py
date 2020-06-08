import copy
import time
import itertools
import cProfile
import random
    

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



def find_move3(node, max_depth):
    
    board = node.board
    
    go = game_over3(board, lines5)
    if go is not None:
        node.value = go
        update_parents2(node)
        return None
    
    if node.depth == max_depth:
        node.value = 0.5 + random.random()*0.1
        update_parents2(node)
        return None
    
    boards_seen = []
    # moves_left = len(moves3(board))
    for move in moves3(board):
        # if node.depth == 0:
            # moves_left -= 1
            # print(moves_left)
        
        if prune2(node) or node.min_value == node.max_value:
            break
        
        new_board_ = new_board3(board, node.player, move)
        
        if new_board_ in boards_seen:
            continue
        
        new_node = Node(new_board_,
                        1-node.player,
                        node,
                        move,
                        node.depth + 1)
        
        boards_seen.append(new_board_)
        
        find_move3(new_node, max_depth)
    
    if node.player == 1:
        node.value = node.min_value
    elif node.player == 0:
        node.value = node.max_value
    if node.depth > 0:
        update_parents2(node)
        
    return node.best_move



def find_move2(node, max_depth):
    
    board = node.board
    
    if game_over(board, lines) is not None:
        node.value = game_over(board, lines)
        update_parents2(node)
        return None
    
    if node.depth == max_depth:
        node.value = 0.5 + random.random()*0.1
        update_parents2(node)
        return None
    
    boards_seen = []
    # moves_left = len(moves(board))
    for move in moves(board):
        # if node.depth == 0:
        #     moves_left -= 1
        #     print(moves_left)
        
        if prune2(node) or node.min_value == node.max_value:
            break
        
        new_board_ = new_board(board, node.player, move)
        
        if new_board_ in boards_seen:
            continue
        
        new_node = Node(new_board_,
                        1-node.player,
                        node,
                        move,
                        node.depth + 1)
        
        boards_seen.append(new_board_)
        
        find_move2(new_node, max_depth)
    
    if node.player == 1:
        node.value = node.min_value
    elif node.player == 0:
        node.value = node.max_value
    if node.depth > 0:
        update_parents2(node)
        
    return node.best_move
    

def update_parents2(node):
    parent = node.parent
    
    if parent is None:
        1 + 1 == 2
    
    if parent.player == 1 and node.value > parent.min_value:
        parent.min_value = node.value
        parent.best_move = node.action
    elif parent.player == 0 and node.value < parent.max_value:
        parent.max_value = node.value
        parent.best_move = node.action
    


def find_move(board, player, max_depth):
    initial_node = Node(board, player, None, None, depth=0)
    frontier = Frontier()
    frontier.add_node(initial_node)
    
    while initial_node.value is None:
        current_node = frontier.next_node()
        current_board = current_node.board
        
        if prune(current_node):
            update_parents(current_node, True)
            continue
        if game_over(current_board, lines) is not None:
            current_node.value = game_over(current_board, lines)
            update_parents(current_node)
        elif current_node.depth == max_depth:
            current_node.value = 0.5 + random.random()*0.1
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


def update_parents(node, prune = False):
    parent = node.parent
    
    if not(prune):
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
    

def moves3(board):
    moves = [(i,j,quadrant, direction)
             for i in range(6)
             for j in range(6)
             if board[6*i+j] == ' '
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


def new_board3(board, player, move):
    i,j, quadrant, direction = move
    new_board = board.copy()
    new_board[6*i+j] = player    
    
    # create array of quadrant of original board to be rotated
    q = [[0,0], [0,1], [1,0], [1,1]][quadrant]
    temp = new_board.copy()
    sub_board = [ [temp[6*(3*q[0]+i)+(3*q[1]+j)]
                    for j in range(3)] for i in range(3)] 
    
    # rotate quadrant and update new board
    if direction == 'c':
        for i in range(3):
            for j in range(3):
                new_board[6*(3*q[0]+i)+(3*q[1]+j)] = sub_board[2-j][i]
                
    if direction == 'ac':
        for i in range(3):
            for j in range(3):
                new_board[6*(3*q[0]+i)+(3*q[1]+j)] = sub_board[j][2-i]   
    
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


def print_board3(board):
    for i in range(11):
        for j in range(11):
            if i % 2 == 1:
                print('-', end = '')
            elif j % 2 == 1:
                print('|', end = '')
            else:
                print(board[int(i/2)*6 + int(j/2)], end = '')
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



def create_lines3():
    lines_h = [[6*i+(j+k) for k in range(5)] 
               for i in range(6) for j in range(2)]
    lines_v = [[6*(i+k)+j for k in range(5)]
               for i in range(2) for j in range(6)]
    lines_d1 = [[6*(i+k)+j+k for k in range(5)] 
                for i in range(2) for j in range(2)]
    lines_d2 = [[6*(i+k)+j-k for k in range(5)] 
                for i in range(2) for j in range(4,6)]
    return lines_h+lines_v+lines_d1+lines_d2
lines3 = create_lines3()


def create_lines4():
    old_lines = create_lines3()
    line_dict = {}
    
    while len(old_lines)>0:
        coordinates = [line[i] for line in old_lines for i in range(5)]
        freq = {}

        for c in coordinates:
            if c not in freq:
                freq[c] = 0
            freq[c] += 1
        
        c,f = max(freq.items(), key=lambda item: item[1])
        
        new_lines = []
        for line in old_lines:
            if c in line:
                new_lines.append(line)
        
        for line in new_lines:
            old_lines.remove(line)
        
        line_dict[c] = new_lines
            
    return line_dict
lines4 = create_lines4()

def create_lines5():
    lines_h = [[6*i+(1+k) for k in range(4)] 
               for i in range(6)]
    h_extra = [[6*i+0, 6*i+5] for i in range(6)]
    
    lines_v = [[6*(1+k)+j for k in range(4)]
               for j in range(6)]
    v_extra = [[6*0+j, 6*5+j] for j in range(6)]
    
    lines_d1 = [[6*(i+k)+j+k for k in range(5)] 
                for i in range(2) for j in range(2)]
    lines_d2 = [[6*(i+k)+j-k for k in range(5)] 
                for i in range(2) for j in range(4,6)]
    lines_d = lines_d1+lines_d2
    
    return [lines_h, h_extra, lines_v, v_extra, lines_d]
lines5 = create_lines5()


    



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


def game_over3_0(board, lines):
    # adapted for lines3
    if any([
            all([
                board[i] == 1 for i in line
                ])
            for line in lines
            ]):
        return 1
    elif any([
            all([
                board[i] == 0 for i in line
                ])
            for line in lines
            ]):
        return 0
    elif len(moves3(board)) == 0:
        return 0.5
    return None


def game_over3_1(board, lines):
    # lines3 + change in algorithm
    for line in lines:
        temp = board[line[0]]
        if temp == ' ':
            continue
        if all([board[line[i]] == temp for i in [1,2,3,4]]):
            return board[line[0]]
    if len(moves3(board)) == 0:
        return 0.5
    return None


def game_over3_2(board, lines_dict):
    # combines with lines4
    for c, lines in lines_dict.items():
        temp = board[c]
        if temp == ' ':
            continue
    
        for line in lines:
            if all([board[line[i]] == temp for i in [0,1,2,3,4]]):
                return temp
            
    if len(moves3(board)) == 0:
        return 0.5
    return None


def game_over3(board, lines_info):
    # combines with lines5
    lines_h, h_extra, lines_v, v_extra, lines_d = lines_info
    
    for i in range(6):
        line = lines_h[i]
        c0, c5 = h_extra[i]
        temp = board[line[0]]
        
        if temp == ' ':
            continue
        if all([board[line[i]] == temp for i in [1,2,3]]):
            if board[c0] == temp or board[c5] == temp:
                return temp
    
    for i in range(6):   
        line = lines_v[i]
        c0, c5 = v_extra[i]
        temp = board[line[0]]
        
        if temp == ' ':
            continue
        if all([board[line[i]] == temp for i in [1,2,3]]):
            if board[c0] == temp or board[c5] == temp:
                return temp
    
    for line in lines_d:
        temp = board[line[0]]
        if temp == ' ':
            continue
        if all([board[line[i]] == temp for i in [1,2,3,4]]):
            return board[line[0]]
    if len(moves3(board)) == 0:
        return 0.5
    return None



def ask_for_move():
    move = input('Please enter your move: ')
    i,j,q,d = move.split(',')
    i,j,q = int(i), int(j), int(q)
    return (i,j,q,d)



def prune(node):
    if node.depth < 2:
        return False
    
    parent = node.parent
    gparent = parent.parent
    
    if node.player == 1 and parent.max_value  < gparent.min_value:
        return True
    elif node.player == 0 and parent.min_value > gparent.max_value:
        return True
    else:
        return False


def prune2(node):
    if node.depth < 2:
        return False
    
    parent = node
    gparent = parent.parent
    
    if node.player == 1 and parent.max_value  < gparent.min_value:
        return True
    elif node.player == 0 and parent.min_value > gparent.max_value:
        return True
    else:
        return False


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
    # empty board
    board0 = [[' ']*6 for _ in range(6)]
    
    # one move left, game to end in a tie
    board1 = [[1,1,1,0,0,0],
              [0,0,0,1,1,1],
              [1,1,1,0,0,0],
              [0,0,0,1,1,1],
              [1,1,1,0,0,0],
              [' ',0,0,1,1,1]]
    
    # 1 to win , and 0 cannot block
    board2 = [[1  ,0  ,0  ,1  ,0  ,1  ],
              [1  ,' ',' ',' ',' ',' '],
              [1  ,1  ,1  ,1  ,0  ,0  ],
              [' ',' ',' ',' ',' ',' '],
              [0,  0,  0,  1,  1,  1  ],
              [' ',1  ,' ',' ',0  ,' ']]
              
    # 0 to win immediately
    board3 = [[0,' ',' ',' ', ' ', ' '],
              [0, ' ', ' ', ' ', ' ', ' '],
              [0, ' ', ' ', ' ', ' ', ' '],
              [0, ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ']]
    
    # 1 to find winning move
    board4 = [[' ', ' ', ' ', ' ', ' ', ' '],
              [' ',1,1, ' ',1, ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ']]
        
    boards = [board0, board1, board2, board3, board4]
    
    new_boards = [ [board[i][j] for i in range(6) for j in range(6)]
                  for board in boards ]
            
    # for board, player in itertools.product(range(1),range(2)):
    #     output, time = timer(find_move, boards[board], player, 2)
    #     print(f"Board: {board}, Player: {player}, Time taken: {time}")
    
    # -------loop through boards using version 2
    # for board, player in itertools.product(range(5),range(2)):
    #     root_node = Node(boards[board], player, None, None, depth=0)
    #     output, time = timer(find_move2, root_node, 2)
    #     print(f"Board: {board}, Player: {player}, Move: {output}, Time taken: {time}")
            
    # ------test finding optimal move for depth 3, version 2
    # node4 = Node(board4, 1, None, None, 0)
    # print(find_move2(node4,3))
    # print(timer(find_move2, node4,3))
    
    
    
    # -------loop through boards using version 3
    # for board, player in itertools.product(range(5),range(2)):
    #     root_node = Node(new_boards[board], player, None, None, depth=0)
    #     output, time = timer(find_move3, root_node, 2)
    #     print(f"Board: {board}, Player: {player}, Time taken: {time}")
    
    # ------test finding optimal move for depth 3, version 3
    node4 = Node(new_boards[4], 1, None, None, 0)
    print(timer(find_move3, node4,3))
    
    
    
    
    
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
    
    
    # testing set of lines3 is correct
    # for line in lines3:
    #     test = new_boards[0].copy()
    #     for l in line:
    #         test[l] = 1
    #     print_board3(test)
    
    
    # test that game over works in version 3
    # print(game_over3(new_boards[3],lines3))
    # new_boards[3][4] = 0
    # print(game_over3(new_boards[3],lines3))
    # print(game_over3(new_boards[4], lines3))
    # new_boards[4][6] = 1
    # new_boards[4][9] = 1
    # print(game_over3(new_boards[4], lines3))
    
    # test new_board works in version 3
    # for move in moves3(new_boards[1]):
    #     print_board3(new_board3(new_boards[1],2, move))
    
    # testing set of lines4 is correct
    # for lines in lines4.values():
    #     for line in lines:
    #         test = new_boards[0].copy()
    #         for l in line:
    #             test[l] = 1
    #         print_board3(test)
    
    
    # test that game over works with lines4
    # print(game_over3(new_boards[3],lines4))
    # new_boards[3][4] = 0
    # print(game_over3(new_boards[3],lines4))
    # print(game_over3(new_boards[4], lines4))
    # new_boards[4][6] = 1
    # new_boards[4][9] = 1
    # print(game_over3(new_boards[4], lines4))
    
    # test that game over works with lines5
    # print(game_over3(new_boards[3],lines5))
    # new_boards[3][24] = 0
    # print(game_over3(new_boards[3],lines5))
    # print(game_over3(new_boards[4], lines5))
    # new_boards[4][6] = 1
    # new_boards[4][9] = 1
    # print(game_over3(new_boards[4], lines5))
    
    return None


def timer(fn, *args):
    t0 = time.time()
    output = fn(*args)
    t1 = time.time()
    return output, t1 - t0

cProfile.run('test()')
# test()
# play()




# --------------No optimisations----------------

# Board: 0, Player: 0, Time taken: 1.5973551273345947
# Board: 0, Player: 1, Time taken: 1.5876989364624023
# Board: 1, Player: 0, Time taken: 0.0011789798736572266
# Board: 1, Player: 1, Time taken: 0.0010318756103515625
# Board: 2, Player: 0, Time taken: 5.049747943878174
# Board: 2, Player: 1, Time taken: 4.941879034042358
# Board: 3, Player: 0, Time taken: 29.29101586341858
# Board: 3, Player: 1, Time taken: 32.09774899482727
# Board: 4, Player: 0, Time taken: 9.555429935455322
# Board: 4, Player: 1, Time taken: 9.259257078170776


# --------------pruning------------------------
# Board: 0, Player: 0, Time taken: 1.345466136932373
# Board: 0, Player: 1, Time taken: 1.3997290134429932
# Board: 1, Player: 0, Time taken: 0.0012030601501464844
# Board: 1, Player: 1, Time taken: 0.0010488033294677734
# Board: 2, Player: 0, Time taken: 5.284406900405884
# Board: 2, Player: 1, Time taken: 4.617739915847778
# Board: 3, Player: 0, Time taken: 26.17604088783264
# Board: 3, Player: 1, Time taken: 29.470968008041382
# Board: 4, Player: 0, Time taken: 8.629671812057495
# Board: 4, Player: 1, Time taken: 8.283491134643555


# ---------------version 2/no frontiers/prune before creating boards
# Board: 0, Player: 0, Time taken: 12.889657735824585
# Board: 0, Player: 1, Time taken: 12.759357213973999
# Board: 1, Player: 0, Time taken: 0.0018579959869384766
# Board: 1, Player: 1, Time taken: 0.001600027084350586
# Board: 2, Player: 0, Time taken: 1.8888230323791504
# Board: 2, Player: 1, Time taken: 1.9842233657836914
# Board: 3, Player: 0, Time taken: 9.999610185623169
# Board: 3, Player: 1, Time taken: 9.902679204940796
# Board: 4, Player: 0, Time taken: 10.221951961517334
# Board: 4, Player: 1, Time taken: 10.249742031097412


# ---------------version 2 + check repeat boards--
# Board: 0, Player: 0, Time taken: 1.0767178535461426
# Board: 0, Player: 1, Time taken: 1.0690727233886719
# Board: 1, Player: 0, Time taken: 0.0011839866638183594
# Board: 1, Player: 1, Time taken: 0.00102996826171875
# Board: 2, Player: 0, Time taken: 1.9064719676971436
# Board: 2, Player: 1, Time taken: 1.861788034439087
# Board: 3, Player: 0, Time taken: 5.333322048187256
# Board: 3, Player: 1, Time taken: 5.413770914077759
# Board: 4, Player: 0, Time taken: 2.98577880859375
# Board: 4, Player: 1, Time taken: 2.9099860191345215


# -------------- above + break if min = max
# Board: 0, Player: 0, Time taken: 1.098992109298706
# Board: 0, Player: 1, Time taken: 1.1168200969696045
# Board: 1, Player: 0, Time taken: 0.0010449886322021484
# Board: 1, Player: 1, Time taken: 0.0011928081512451172
# Board: 2, Player: 0, Time taken: 0.32472896575927734
# Board: 2, Player: 1, Time taken: 0.34493279457092285
# Board: 3, Player: 0, Time taken: 0.141754150390625
# Board: 3, Player: 1, Time taken: 0.897752046585083
# Board: 4, Player: 0, Time taken: 3.121652126312256
# Board: 4, Player: 1, Time taken: 2.9370980262756348
# depth 3 solution. ((0, 4, 1, 'ac'), 59.11349701881409) ~7mins total


# -------------- version3. rank1 list instead of rank2 list
# Board: 0, Player: 0, Time taken: 0.40738892555236816
# Board: 0, Player: 1, Time taken: 0.41133594512939453
# Board: 1, Player: 0, Time taken: 0.0005202293395996094
# Board: 1, Player: 1, Time taken: 0.0004508495330810547
# Board: 2, Player: 0, Time taken: 0.17560601234436035
# Board: 2, Player: 1, Time taken: 0.16147398948669434
# Board: 3, Player: 0, Time taken: 0.06450676918029785
# Board: 3, Player: 1, Time taken: 0.42441606521606445
# Board: 4, Player: 0, Time taken: 1.4196019172668457
# Board: 4, Player: 1, Time taken: 1.418367862701416
# depth 3 solution. ((0, 4, 1, 'ac'), 30.73452377319336) ~3.5 mins total

 #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 #        1    0.000    0.000   38.751   38.751 <string>:1(<module>)
 #        3    0.000    0.000    0.000    0.000 iostream.py:197(schedule)
 #        2    0.000    0.000    0.000    0.000 iostream.py:309(_is_master_process)
 #        2    0.000    0.000    0.000    0.000 iostream.py:322(_schedule_flush)
 #        2    0.000    0.000    0.000    0.000 iostream.py:384(write)
 #        3    0.000    0.000    0.000    0.000 iostream.py:93(_event_pipe)
 #   299209    0.220    0.000    0.220    0.000 pentago.py:122(__init__)
 # 299209/1    2.726    0.000   38.751   38.751 pentago.py:151(find_move3)
 #   299208    0.142    0.000    0.142    0.000 pentago.py:250(update_parents2)
 #   300963    0.229    0.000    9.265    0.000 pentago.py:346(moves3)
 #   300963    9.036    0.000    9.036    0.000 pentago.py:347(<listcomp>) LIST OF MOVES
 #   460503    2.395    0.000    4.527    0.000 pentago.py:381(new_board3)
 #   460503    0.814    0.000    1.987    0.000 pentago.py:389(<listcomp>) SUB_BOARD AS RANK2 LIST
 #   299778    1.469    0.000   30.783    0.000 pentago.py:480(game_over3) DETERMINING GAME OVER
 #   299778    4.163    0.000   10.119    0.000 pentago.py:481(<listcomp>)
 #  9592896    4.852    0.000    4.852    0.000 pentago.py:482(<listcomp>)
 #   298640    4.071    0.000    9.808    0.000 pentago.py:488(<listcomp>)
 #  9556480    4.724    0.000    4.724    0.000 pentago.py:489(<listcomp>)
 #   461073    0.200    0.000    0.200    0.000 pentago.py:523(prune2)
 #        1    0.000    0.000   38.751   38.751 pentago.py:566(test)
 #        1    0.000    0.000    0.000    0.000 pentago.py:568(<listcomp>)
 #        1    0.000    0.000    0.000    0.000 pentago.py:606(<listcomp>)
 #        1    0.000    0.000   38.751   38.751 pentago.py:708(timer)
 #        3    0.000    0.000    0.000    0.000 socket.py:342(send)
 #        3    0.000    0.000    0.000    0.000 threading.py:1017(_wait_for_tstate_lock)
 #        3    0.000    0.000    0.000    0.000 threading.py:1071(is_alive)
 #        3    0.000    0.000    0.000    0.000 threading.py:513(is_set)
 # 19149376    2.118    0.000    2.118    0.000 {built-in method builtins.all}
 #   598418    0.157    0.000    0.157    0.000 {built-in method builtins.any}
 #        1    0.000    0.000   38.751   38.751 {built-in method builtins.exec}
 #        2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
 #   298640    0.037    0.000    0.037    0.000 {built-in method builtins.len}
 #        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
 #        2    0.000    0.000    0.000    0.000 {built-in method posix.getpid}
 #        2    0.000    0.000    0.000    0.000 {built-in method time.time}
 #        3    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
 #        3    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
 #   299208    0.039    0.000    0.039    0.000 {method 'append' of 'list' objects}
 #   921006    0.145    0.000    0.145    0.000 {method 'copy' of 'list' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 #   296317    0.042    0.000    0.042    0.000 {method 'random' of '_random.Random' objects}



# -------------- version3. + game_over3_1
# Board: 0, Player: 0, Time taken: 0.29244232177734375
# Board: 0, Player: 1, Time taken: 0.2838928699493408
# Board: 1, Player: 0, Time taken: 0.0004999637603759766
# Board: 1, Player: 1, Time taken: 0.00033402442932128906
# Board: 2, Player: 0, Time taken: 0.10118913650512695
# Board: 2, Player: 1, Time taken: 0.10771417617797852
# Board: 3, Player: 0, Time taken: 0.03592395782470703
# Board: 3, Player: 1, Time taken: 0.26180291175842285
# Board: 4, Player: 0, Time taken: 0.9436769485473633
# Board: 4, Player: 1, Time taken: 0.9159080982208252
# cProfile for depth 3
   # 299778    3.458    0.000   14.519    0.000 pentago.py:500(game_over3)


# -------------- above+call game_over only once per cycle
   # 299209    3.335    0.000   14.162    0.000 pentago.py:532(game_over3)



# -------------- version3. + lines4
# Board: 0, Player: 0, Time taken: 0.26334691047668457
# Board: 0, Player: 1, Time taken: 0.2673959732055664
# Board: 1, Player: 0, Time taken: 0.0003211498260498047
# Board: 1, Player: 1, Time taken: 0.0003368854522705078
# Board: 2, Player: 0, Time taken: 0.10031986236572266
# Board: 2, Player: 1, Time taken: 0.10820603370666504
# Board: 3, Player: 0, Time taken: 0.03513503074645996
# Board: 3, Player: 1, Time taken: 0.24969196319580078
# Board: 4, Player: 0, Time taken: 0.9256749153137207
# Board: 4, Player: 1, Time taken: 0.9308981895446777
# cProfile for depth 3
