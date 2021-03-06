import copy
import time
import itertools
import cProfile
import random
    
random.seed(0)

class Node():
    def __init__(self, board, player, parent, action, depth):
        self.board = board
        self.player = player
        self.parent = parent
        self.action = action
        self.depth = depth
        self.max_value = 1
        self.min_value = 0
        self.value = None
        self.best_move = None
        if depth == 0:
            self.all_boards = {}
        else:
            self.all_boards = parent.all_boards

def find_move(node, max_depth):   
    board = node.board
    board_tuple = tuple(board)
    
    if board_tuple in node.all_boards:
        node.value = node.all_boards[board_tuple]
        update_parents(node)
        return None
    
    go = game_over(board, lines)
    if go is not None:
        node.value = go
        node.all_boards[board_tuple] = node.value
        update_parents(node)
        return None
    
    if node.depth == max_depth:
        node.value = 0.5 + random.random()*0.1
        node.all_boards[board_tuple] = node.value
        update_parents(node)
        return None
    
    # moves_left = len(moves(board))
    for move in moves(board):        
        # if node.depth == 0:
            # moves_left -= 1
            # print(moves_left)
        
        if prune(node):
            return None
        
        if node.min_value == node.max_value:
            break
        
        new_board_ = new_board(board, node.player, move)
        new_node = Node(new_board_,
                        1-node.player,
                        node,
                        move,
                        node.depth + 1)
        
        find_move(new_node, max_depth)
    
    if node.player == 1:
        node.value = node.min_value
    elif node.player == 0:
        node.value = node.max_value
    if node.depth > 0:
        update_parents(node)
    node.all_boards[board_tuple] = node.value
        
    return node.best_move
    

def update_parents(node):
    parent = node.parent
    
    if parent.player == 1 and node.value > parent.min_value:
        parent.min_value = node.value
        parent.best_move = node.action
        parent.best_child = node
    elif parent.player == 0 and node.value < parent.max_value:
        parent.max_value = node.value
        parent.best_move = node.action
        parent.best_child = node
            

def moves(board):
    moves = [(i,j,quadrant, direction)
             for i in range(6)
             for j in range(6)
             if board[6*i+j] == ' '
             for quadrant in range(4)
             for direction in ['c', 'ac']]
    return moves


def new_board(board, player, move):
    i,j, quadrant, direction = move
    new_board = board.copy()
    new_board[6*i+j] = player 
    
    # create quadrant to be rotated
    q = [[0,0], [0,1], [1,0], [1,1]][quadrant]
    temp = new_board.copy()
    sub_board = [ temp[6*(3*q[0]+(ij//3))+(3*q[1]+(ij%3))]
                  for ij in range(9)]
                
    # rotate quadrant and update new board
    if direction == 'c':
        for i in range(3):
            for j in range(3):
                new_board[6*(3*q[0]+i)+(3*q[1]+j)] = sub_board[3*(2-j)+i]
                
    if direction == 'ac':
        for i in range(3):
            for j in range(3):
                new_board[6*(3*q[0]+i)+(3*q[1]+j)] = sub_board[3*j+(2-i)] 
    
    return new_board


def print_board(board):
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


def create_lines1():
    lines_h = [[6*i+(j+k) for k in range(5)] 
               for i in range(6) for j in range(2)]
    lines_v = [[6*(i+k)+j for k in range(5)]
               for i in range(2) for j in range(6)]
    lines_d1 = [[6*(i+k)+j+k for k in range(5)] 
                for i in range(2) for j in range(2)]
    lines_d2 = [[6*(i+k)+j-k for k in range(5)] 
                for i in range(2) for j in range(4,6)]
    return lines_h+lines_v+lines_d1+lines_d2

def create_lines2():
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

def create_lines3():
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

lines = create_lines1()


def game_over1(board, lines):
    # lines1 + change in algorithm
    for line in lines:
        temp = board[line[0]]
        if temp == ' ':
            continue
        if all([board[line[i]] == temp for i in [1,2,3,4]]):
            return board[line[0]]
    if len(moves(board)) == 0:
        return 0.5
    return None


def game_over2(board, lines_dict):
    # combines with lines4
    for c, lines in lines_dict.items():
        temp = board[c]
        if temp == ' ':
            continue
    
        for line in lines:
            if all([board[line[i]] == temp for i in [0,1,2,3,4]]):
                return temp
            
    if len(moves(board)) == 0:
        return 0.5
    return None


def game_over3(board, lines_info):
    # combines with lines3
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
    if len(moves(board)) == 0:
        return 0.5
    return None

game_over = game_over1



def ask_for_move():
    move = input('Please enter your move: ')
    i,j,q,d = move.split(',')
    i,j,q = int(i), int(j), int(q)
    return (i,j,q,d)

def prune(node):
    if node.depth == 0:
        return False

    parent = node.parent
    if node.player == 0 and node.max_value < parent.min_value:
        return True
    elif node.player == 1 and node.min_value > parent.max_value:
        return True
    else:
        return False

def play():
    board = [' ' for _ in range(36)]
    ai =  False
    player = 1
    
    while game_over(board, lines) is None:
        print('')
        print_board(board)
        print(f'Current player is: {player} \n')
        
        if ai == False:
            move = ask_for_move()
            ai = True
        else:
            print('ai is thinking...')
            node = Node(board, player, None, None, 0)
            move = find_move(node, 2)
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
    board0 = [' ' for _ in range(36)]
    
    # one move left, game to end in a tie
    board1 = [1,1,1,0,0,0,
              0,0,0,1,1,1,
              1,1,1,0,0,0,
              0,0,0,1,1,1,
              1,1,1,0,0,0,
              ' ',0,0,1,1,1]
    
    # 1 to win , and 0 cannot block
    board2 = [1  ,0  ,0  ,1  ,0  ,1  ,
              1  ,' ',' ',' ',' ',' ',
              1  ,1  ,1  ,1  ,0  ,0  ,
              ' ',' ',' ',' ',' ',' ',
              0,  0,  0,  1,  1,  1  ,
              ' ',1  ,' ',' ',0  ,' ']
              
    # 0 to win immediately
    board3 = [0,' ',' ',' ', ' ', ' ',
              0, ' ', ' ', ' ', ' ', ' ',
              0, ' ', ' ', ' ', ' ', ' ',
              0, ' ', ' ', ' ', ' ', ' ',
              ' ', ' ', ' ', ' ', ' ', ' ',
              ' ', ' ', ' ', ' ', ' ', ' ']
    
    # 1 to find winning move
    board4 = [' ', ' ', ' ', ' ', ' ', ' ',
              ' ',1,1, ' ',1, ' ',
              ' ', ' ', ' ', ' ', ' ', ' ',
              ' ', ' ', ' ', ' ', ' ', ' ',
              ' ', ' ', ' ', ' ', ' ', ' ',
              ' ', ' ', ' ', ' ', ' ', ' ']
        
    boards = [board0, board1, board2, board3, board4]
            
    # -------loop through boards
    # for board, player in itertools.product(range(5),range(2)):
        # root_node = Node(boards[board], player, None, None, depth=0)
        # output, time = timer(find_move, root_node, 2)
        # print(f"Board: {board}, Player: {player}, Time taken: {time}")
        # print(f"Board: {board}, Player: {player}, Output: {output}, Time taken: {time}")
    
    # ------test finding optimal move for depth 3
    # node4 = Node(boards[4], 1, None, None, 0)
    # print(timer(find_move, node4,3))
    
    # ------test finding optimal move for depth 4
    # node4 = Node(boards[4], 0, None, None, 0)
    # print(timer(find_move, node4,4))
    
    
    # -------test game over
    # print(game_over3(boards[3],lines3))
    # new_boards[3][4] = 0
    # print(game_over3(boards[3],lines3))
    # print(game_over3(boards[4], lines3))
    # new_boards[4][6] = 1
    # new_boards[4][9] = 1
    # print(game_over3(boards[4], lines3))
    
   
    # --------- lines is correc
    # for lines in lines4.values():
    #     for line in lines:
    #         test = new_boards[0].copy()
    #         for l in line:
    #             test[l] = 1
    #         print_board3(test)
    
    return None

def timer(fn, *args):
    t0 = time.time()
    output = fn(*args)
    t1 = time.time()
    return output, t1 - t0

# cProfile.run('test()')
test()
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
# cProfile for depth 3, was similar to above. 14 seconds


# -------------- version3. + lines5
# cProfile for depth 3
   # 299209    3.409    0.000   14.048    0.000 pentago.py:582(game_over3)
   
 # -------------- tidied up, and fixed prune  
# Board: 0, Player: 0, Time taken: 0.08965802192687988
# Board: 0, Player: 1, Time taken: 0.06820201873779297
# Board: 1, Player: 0, Time taken: 0.0002720355987548828
# Board: 1, Player: 1, Time taken: 0.0002040863037109375
# Board: 2, Player: 0, Time taken: 0.10023093223571777
# Board: 2, Player: 1, Time taken: 0.053900957107543945
# Board: 3, Player: 0, Time taken: 0.3132359981536865
# Board: 3, Player: 1, Time taken: 1.138319730758667
# Board: 4, Player: 0, Time taken: 0.2041919231414795
# Board: 4, Player: 1, Time taken: 0.3106269836425781
# cprofile for depth3. Game_over and moves are big ones.

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    3.189    3.189 <string>:1(<module>)
#         2    0.000    0.000    0.000    0.000 _weakrefset.py:38(_remove)
#         3    0.000    0.000    0.000    0.000 iostream.py:197(schedule)
#         2    0.000    0.000    0.000    0.000 iostream.py:309(_is_master_process)
#         2    0.000    0.000    0.000    0.000 iostream.py:322(_schedule_flush)
#         2    0.000    0.000    0.000    0.000 iostream.py:384(write)
#         3    0.000    0.000    0.000    0.000 iostream.py:93(_event_pipe)
#     63374    0.358    0.000    0.673    0.000 pentago.py:107(new_board)
#    190122    0.171    0.000    0.171    0.000 pentago.py:115(<listcomp>)
#     39342    0.497    0.000    2.078    0.000 pentago.py:203(game_over1)
#    411457    0.224    0.000    0.224    0.000 pentago.py:209(<listcomp>)
#   39342/1    0.301    0.000    3.189    3.189 pentago.py:22(find_move)
#     64334    0.031    0.000    0.031    0.000 pentago.py:278(prune)
#         1    0.000    0.000    3.189    3.189 pentago.py:318(test)
#         1    0.000    0.000    0.000    0.000 pentago.py:320(<listcomp>)
#         1    0.000    0.000    0.000    0.000 pentago.py:356(<listcomp>)
#         1    0.000    0.000    3.189    3.189 pentago.py:391(timer)
#     39341    0.029    0.000    0.029    0.000 pentago.py:71(update_parents)
#     39342    0.030    0.000    0.030    0.000 pentago.py:9(__init__)
#     40003    0.032    0.000    1.332    0.000 pentago.py:97(moves)
#     40003    1.300    0.000    1.300    0.000 pentago.py:98(<listcomp>)
#         3    0.000    0.000    0.000    0.000 socket.py:342(send)
#         3    0.000    0.000    0.000    0.000 threading.py:1017(_wait_for_tstate_lock)
#         3    0.000    0.000    0.000    0.000 threading.py:1071(is_alive)
#         3    0.000    0.000    0.000    0.000 threading.py:513(is_set)
#    411457    0.054    0.000    0.054    0.000 {built-in method builtins.all}
#         1    0.000    0.000    3.189    3.189 {built-in method builtins.exec}
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
#     38968    0.005    0.000    0.005    0.000 {built-in method builtins.len}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#         2    0.000    0.000    0.000    0.000 {built-in method posix.getpid}
#         2    0.000    0.000    0.000    0.000 {built-in method time.time}
#         3    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
#         3    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
#     39341    0.006    0.000    0.006    0.000 {method 'append' of 'list' objects}
#    126748    0.022    0.000    0.022    0.000 {method 'copy' of 'list' objects}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#         2    0.000    0.000    0.000    0.000 {method 'discard' of 'set' objects}
#     37933    0.006    0.000    0.006    0.000 {method 'random' of '_random.Random' objects}


# heuristic = 0.5 always, without all_boards, with boards seen
  # 299209    3.491    0.000   14.883    0.000 pentago.py:215(game_over1)
  
  # heuristic = 0.5 always, with all boards, without boards seen
  # 30815    0.373    0.000    1.559    0.000 pentago.py:215(game_over1)
  
# with both

  
 # -------------- with all_boards
# Board: 0, Player: 0, Time taken: 0.08091402053833008
# Board: 0, Player: 1, Time taken: 0.08608317375183105
# Board: 1, Player: 0, Time taken: 0.0002551078796386719
# Board: 1, Player: 1, Time taken: 0.0002338886260986328
# Board: 2, Player: 0, Time taken: 0.08531403541564941
# Board: 2, Player: 1, Time taken: 0.03759002685546875
# Board: 3, Player: 0, Time taken: 0.29084110260009766
# Board: 3, Player: 1, Time taken: 0.6572558879852295
# Board: 4, Player: 0, Time taken: 0.16455411911010742
# Board: 4, Player: 1, Time taken: 0.14598584175109863 

  #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  #       1    0.002    0.002    2.199    2.199 <string>:1(<module>)
  #       3    0.000    0.000    0.000    0.000 iostream.py:197(schedule)
  #       2    0.000    0.000    0.000    0.000 iostream.py:309(_is_master_process)
  #       2    0.000    0.000    0.000    0.000 iostream.py:322(_schedule_flush)
  #       2    0.000    0.000    0.000    0.000 iostream.py:384(write)
  #       3    0.000    0.000    0.000    0.000 iostream.py:93(_event_pipe)
  #   18910    0.015    0.000    0.609    0.000 pentago.py:109(moves)
  #   18910    0.595    0.000    0.595    0.000 pentago.py:110(<listcomp>)
  #   84640    0.433    0.000    0.813    0.000 pentago.py:119(new_board)
  #   84640    0.146    0.000    0.354    0.000 pentago.py:127(<listcomp>)
  #   17896    0.218    0.000    0.909    0.000 pentago.py:215(game_over1)
  #  176723    0.092    0.000    0.092    0.000 pentago.py:221(<listcomp>)
  # 84641/1    0.284    0.000    2.197    2.197 pentago.py:25(find_move)
  #   85541    0.037    0.000    0.037    0.000 pentago.py:290(prune)
  #       1    0.000    0.000    2.197    2.197 pentago.py:331(test)
  #       1    0.000    0.000    0.000    0.000 pentago.py:333(<listcomp>)
  #       5    0.000    0.000    0.000    0.000 pentago.py:369(<listcomp>)
  #       1    0.000    0.000    2.197    2.197 pentago.py:404(timer)
  #   84640    0.049    0.000    0.049    0.000 pentago.py:83(update_parents)
  #   84641    0.067    0.000    0.067    0.000 pentago.py:9(__init__)
  #       3    0.000    0.000    0.000    0.000 socket.py:342(send)
  #       3    0.000    0.000    0.000    0.000 threading.py:1017(_wait_for_tstate_lock)
  #       3    0.000    0.000    0.000    0.000 threading.py:1071(is_alive)
  #       3    0.000    0.000    0.000    0.000 threading.py:513(is_set)
  #  176723    0.022    0.000    0.022    0.000 {built-in method builtins.all}
  #       1    0.000    0.000    2.199    2.199 {built-in method builtins.exec}
  #       2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
  #   17837    0.002    0.000    0.002    0.000 {built-in method builtins.len}
  #       1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
  #       2    0.000    0.000    0.000    0.000 {built-in method posix.getpid}
  #       2    0.000    0.000    0.000    0.000 {built-in method time.time}
  #       3    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
  #       3    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
  #  169280    0.026    0.000    0.026    0.000 {method 'copy' of 'list' objects}
  #       1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  #   16764    0.003    0.000    0.003    0.000 {method 'random' of '_random.Random' objects}
  
  # ================fixing bug in all_boards interaction with prune
# Board: 0, Player: 0, Time taken: 0.2888009548187256
# Board: 0, Player: 1, Time taken: 0.15045881271362305
# Board: 1, Player: 0, Time taken: 0.00028705596923828125
# Board: 1, Player: 1, Time taken: 0.0002300739288330078
# Board: 2, Player: 0, Time taken: 0.0822603702545166
# Board: 2, Player: 1, Time taken: 0.03888416290283203
# Board: 3, Player: 0, Time taken: 0.30017614364624023
# Board: 3, Player: 1, Time taken: 0.7593698501586914
# Board: 4, Player: 0, Time taken: 0.3503570556640625
# Board: 4, Player: 1, Time taken: 0.3380570411682129
 #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 #        1    0.000    0.000    3.193    3.193 <string>:1(<module>)
 #        3    0.000    0.000    0.000    0.000 iostream.py:197(schedule)
 #        2    0.000    0.000    0.000    0.000 iostream.py:309(_is_master_process)
 #        2    0.000    0.000    0.000    0.000 iostream.py:322(_schedule_flush)
 #        2    0.000    0.000    0.000    0.000 iostream.py:384(write)
 #        3    0.000    0.000    0.000    0.000 iostream.py:93(_event_pipe)
 #   150662    0.125    0.000    0.125    0.000 pentago.py:10(__init__)
 #   150661    0.806    0.000    1.515    0.000 pentago.py:102(new_board)
 #   150661    0.277    0.000    0.661    0.000 pentago.py:110(<listcomp>)
 #    14905    0.201    0.000    0.816    0.000 pentago.py:198(game_over1)
 #   148402    0.083    0.000    0.083    0.000 pentago.py:204(<listcomp>)
 # 150662/1    0.507    0.000    3.193    3.193 pentago.py:25(find_move)
 #   153546    0.067    0.000    0.067    0.000 pentago.py:273(prune)
 #        1    0.000    0.000    3.193    3.193 pentago.py:314(test)
 #        1    0.000    0.000    0.000    0.000 pentago.py:316(<listcomp>)
 #        5    0.000    0.000    0.000    0.000 pentago.py:352(<listcomp>)
 #        1    0.000    0.000    3.193    3.193 pentago.py:392(timer)
 #   147961    0.061    0.000    0.061    0.000 pentago.py:79(update_parents)
 #    17798    0.015    0.000    0.609    0.000 pentago.py:92(moves)
 #    17798    0.594    0.000    0.594    0.000 pentago.py:93(<listcomp>)
 #        3    0.000    0.000    0.000    0.000 socket.py:342(send)
 #        3    0.000    0.000    0.000    0.000 threading.py:1017(_wait_for_tstate_lock)
 #        3    0.000    0.000    0.000    0.000 threading.py:1071(is_alive)
 #        3    0.000    0.000    0.000    0.000 threading.py:513(is_set)
 #   148402    0.020    0.000    0.020    0.000 {built-in method builtins.all}
 #        1    0.000    0.000    3.193    3.193 {built-in method builtins.exec}
 #        2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
 #    14843    0.002    0.000    0.002    0.000 {built-in method builtins.len}
 #        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
 #        2    0.000    0.000    0.000    0.000 {built-in method posix.getpid}
 #        2    0.000    0.000    0.000    0.000 {built-in method time.time}
 #        3    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
 #        3    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
 #   301322    0.048    0.000    0.048    0.000 {method 'copy' of 'list' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 #    11888    0.002    0.000    0.002    0.000 {method 'random' of '_random.Random' objects}


# new board updated to only have rank1 arrays
 #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 #        1    0.000    0.000    2.831    2.831 <string>:1(<module>)
 #        3    0.000    0.000    0.000    0.000 iostream.py:197(schedule)
 #        2    0.000    0.000    0.000    0.000 iostream.py:309(_is_master_process)
 #        2    0.000    0.000    0.000    0.000 iostream.py:322(_schedule_flush)
 #        2    0.000    0.000    0.000    0.000 iostream.py:384(write)
 #        3    0.000    0.000    0.000    0.000 iostream.py:93(_event_pipe)
 #   157217    0.122    0.000    0.122    0.000 pentago.py:10(__init__)
 #   157216    0.810    0.000    1.269    0.000 pentago.py:102(new_board)
 #   157216    0.410    0.000    0.410    0.000 pentago.py:110(<listcomp>)
 #    14925    0.186    0.000    0.763    0.000 pentago.py:198(game_over1)
 #   148890    0.078    0.000    0.078    0.000 pentago.py:204(<listcomp>)
 # 157217/1    0.474    0.000    2.831    2.831 pentago.py:25(find_move)
 #   159519    0.065    0.000    0.065    0.000 pentago.py:273(prune)
 #        1    0.000    0.000    2.831    2.831 pentago.py:314(test)
 #        1    0.000    0.000    0.000    0.000 pentago.py:316(<listcomp>)
 #        5    0.000    0.000    0.000    0.000 pentago.py:352(<listcomp>)
 #        1    0.000    0.000    2.831    2.831 pentago.py:392(timer)
 #   155098    0.061    0.000    0.061    0.000 pentago.py:79(update_parents)
 #    17240    0.013    0.000    0.554    0.000 pentago.py:92(moves)
 #    17240    0.540    0.000    0.540    0.000 pentago.py:93(<listcomp>)
 #        3    0.000    0.000    0.000    0.000 socket.py:342(send)
 #        3    0.000    0.000    0.000    0.000 threading.py:1017(_wait_for_tstate_lock)
 #        3    0.000    0.000    0.000    0.000 threading.py:1071(is_alive)
 #        3    0.000    0.000    0.000    0.000 threading.py:513(is_set)
 #   148890    0.019    0.000    0.019    0.000 {built-in method builtins.all}
 #        1    0.000    0.000    2.831    2.831 {built-in method builtins.exec}
 #        2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
 #    14863    0.002    0.000    0.002    0.000 {built-in method builtins.len}
 #        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
 #        2    0.000    0.000    0.000    0.000 {built-in method posix.getpid}
 #        2    0.000    0.000    0.000    0.000 {built-in method time.time}
 #        3    0.000    0.000    0.000    0.000 {method 'acquire' of '_thread.lock' objects}
 #        3    0.000    0.000    0.000    0.000 {method 'append' of 'collections.deque' objects}
 #   314432    0.048    0.000    0.048    0.000 {method 'copy' of 'list' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 #    12486    0.002    0.000    0.002    0.000 {method 'random' of '_random.Random' objects}


