from random import *
from puzzle import GameGrid

#Helper Functions
def accumulate(fn, initial, seq):
    if not seq:
        return initial
    else:
        return fn(seq[0],
                  accumulate(fn, initial, seq[1:]))

def flatten(mat):
    return [num for row in mat for num in row]

#Basic Matrix Setup
def new_game_matrix(n):
    matrix = []
    for i in range(n):
        matrix.append([0]*n)
    return matrix
    

def has_zero(mat):
    if 0 in flatten(mat):
        return True
    else:
        return False

def add_two(mat):
    if not has_zero(mat):
        return mat
    else:
        row=randint(0,len(mat)-1)
        col=randint(0,len(mat[0])-1)
        if mat[row][col]==0:
            mat[row][col]=2
            return mat
        else:
            return add_two(mat)

def game_status(mat):
    def have_moves(mat):
        for i in mat:
            for j in range(len(mat)-1):
                if i[j]==i[j+1]:
                    return True
                else:
                    continue
        for k in range(len(mat)-1):
            for l in range(len(mat)):
                if mat[k][l]==mat[k+1][l]:
                    return True
                else:
                    continue
        return False
    if 2048 in flatten(mat):
        return "win"
    elif has_zero(mat)==False and have_moves(mat)==False:
        return "lose"
    else:
        return "not over"

#Basic Matrix Operations
def transpose(mat):
    trans=[]
    for i in range(len(mat[0])):
        row=[]
        for j in mat:
            row.append(j[i])
        trans.append(row)
    return trans


def reverse(mat):
    new=[]
    newer=[]
    for i in mat:
        for j in range(len(i)):
            new.extend([i[len(i)-1-j]])
        newer.append(new)
        new=[]
    return newer

#Game Logic Based on Movements
def score_increment(matPrev, matFinal):
    first = flatten(matPrev)
    second = flatten(matFinal)
    for i in second:
        if i in first and i!=0:
            first.remove(i)
    sumf = 0
    for i in first:
        sumf += i
    return sumf

def push_to_left(row):
    new=[0,]*len(row)
    for i in range(len(row)):
        position=i
        if row[i]==0:
            continue
        else:
            while new[position-1]==0 and position>0:
                position=position-1
            new[position]=row[i]            
    return new
    
def merge_left(mat):
    newer=[]
    score = 0
    for i in mat:
        a=push_to_left(i)
        for j in range(len(a)-1):
            if a[j]==a[j+1]:     
                a[j]=a[j]*2
                a[j+1]=0
                score += a[j]
            else:
                continue
        for k in range(len(a)):
            if a[k]==0:
                a.remove(0)
                a.extend([0])
            else:
                continue
        newer.append(a)
    return (newer, newer!=mat, score)

def merge_right(mat):
    first = merge_left(reverse(mat))
    result = reverse(first[0])
    return (result, first[1], first[2])

def merge_up(mat):
    first = merge_left(transpose(mat))
    result = transpose(first[0])
    return (result, first[1], first[2])

def merge_down(mat):
    first = merge_left(reverse(transpose(mat)))
    result = transpose(reverse(first[0]))
    return (result, first[1], first[2])

def make_state(matrix, total_score):
    return [matrix, total_score]

def get_matrix(state):
    return state[0]

def get_score(state):
    return state[1]

#Game Operations
def make_new_game(n):
    b=add_two(new_game_matrix(n))
    c=add_two(b)
    return make_state(c,0)

def make_state(matrix, total_score):
    return [matrix, total_score]

def get_matrix(state):
    return state[0]

def get_score(state):
    return state[1]

def make_new_game(n):
    b=add_two(new_game_matrix(n))
    c=add_two(b)
    return make_state(c,0)

def left(state):
    return instruction('left', state)

def right(state):
    return instruction('right', state)

def up(state):
    return instruction('up', state)

def down(state):
    return instruction('down', state)

def instruction(instruct, state):
    if instruct == 'down':
        a = merge_down(get_matrix(state))
    elif instruct == 'up':
        a = merge_up(get_matrix(state))
    elif instruct == 'right':
        a = merge_right(get_matrix(state))
    else:
        a = merge_left(get_matrix(state))
    if a[0]!=get_matrix(state):
        b=add_two(a[0])
        return (make_state(b, get_score(state) + a[2]),a[1])
    else:
        return (make_state(get_matrix(state), get_score(state)),a[1])

game_logic = {
    'make_new_game': make_new_game,
    'game_status': game_status,
    'get_score': get_score,
    'get_matrix': get_matrix,
    'up': up,
    'down': down,
    'left': left,
    'right': right,
    'undo': lambda state: (state, False)
}

gamegrid = GameGrid(game_logic)