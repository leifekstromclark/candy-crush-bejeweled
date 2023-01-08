import stddraw
import random
import time

def draw_circle(x, y, match):
    stddraw.setPenColor(stddraw.color.MAGENTA)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledCircle(x+10, y+10, 8)

def draw_square(x, y, match):
    stddraw.setPenColor(stddraw.color.YELLOW)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledRectangle(x+2, y+2, 16, 16)

def draw_triangle(x, y, match):
    stddraw.setPenColor(stddraw.color.ORANGE)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledPolygon((x+2, x+10, x+18), (y+2, y+18, y+2))

def draw_diamond(x, y, match):
    stddraw.setPenColor(stddraw.color.DARK_BLUE)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledPolygon((x+2, x+10, x+18, x+10), (y+10, y+2, y+10, y+18))

def draw_para(x, y, match):
    stddraw.setPenColor(stddraw.color.DARK_RED)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledPolygon((x+2, x+6, x+18, x+14), (y+6, y+14, y+14, y+6))

def draw_pentagon(x, y, match):
    stddraw.setPenColor(stddraw.color.DARK_GREEN)
    if match:
        stddraw.setPenColor(stddraw.color.WHITE)
    stddraw.filledPolygon((x+2, x+10, x+18, x+14, x+6), (y+12, y+18, y+12, y+2, y+2))

def draw_selector(select):
    stddraw.rectangle(select[0]*20, select[1]*20+10, 20, 20)

def shift_board(board):
    shifts = {}
    for i in range(7):
        for k in range(9):
            if board[i][k] == 0:
                for j in range(k, 8):
                    board[i][j] = board[i][j+1]
                board[i][8] = random.randint(1, 6)
                shifts[i] = k
                break
    return board, shifts

def switch(field, a, b):
    h = field[a[0]][a[1]]
    field[a[0]][a[1]] = field[b[0]][b[1]]
    field[b[0]][b[1]] = h
    return field

def check_matches(field, select=None, move_to=None):
    matches = []
    if select is not None and move_to is not None:
        field = switch(field, select, move_to)
    for i in range(7):
        for k in range(9):
            if 0 < k < 8:
                if field[i][k-1] == field[i][k] == field[i][k+1]:
                    matches += ((i, k-1), (i, k), (i, k+1))
            if 0 < i < 6:
                if field[i-1][k] == field[i][k] == field[i+1][k]:
                    matches += ((i-1, k), (i, k), (i+1, k))
    if select is not None and move_to is not None:
        field = switch(field, move_to, select)
    return set(matches)

stddraw.setCanvasSize(700, 950)            
stddraw.setXscale(0, 140)
stddraw.setYscale(0, 190)

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

falling = True
matches = []
anim_counter = 0
score = 0
moves = 25
select = None

while True:
    stddraw.clear(stddraw.color.BLACK)
    if moves == 0 and len(matches) == 0 and not falling:
        if stddraw.mousePressed():
            board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

            falling = True
            matches = []
            anim_counter = 0
            score = 0
            moves = 25
            select = None

        stddraw.text(70, 120, 'Game Over!')
        stddraw.text(70, 100, 'Final Score: ' + str(score))
        stddraw.text(70, 80, 'Click Anywhere To Play Again')
    
    else:
        if falling:
            if anim_counter == 0:
                board, shifts = shift_board(board)
                if len(shifts) == 0:
                    falling = False
                    matches = check_matches(board)
                    if len(matches) != 0:
                        anim_counter = 5
                else:
                    anim_counter = 5
            else:
                anim_counter -= 1

        elif len(matches) != 0:
            if anim_counter == 0:
                for coords in matches:
                    score += 1
                    board[coords[0]][coords[1]] = 0
                matches = []
                falling = True
            else:
                anim_counter -= 1

        else:
            if stddraw.mousePressed():
                if select is None and 10 < stddraw.mouseY() < 190 and 0 < stddraw.mouseX() < 140:
                    select = (int(stddraw.mouseX() // 20), int((stddraw.mouseY() - 10) // 20))
                elif select is not None:
                    if 10 < stddraw.mouseY() < 190 and 0 < stddraw.mouseX() < 140:
                        x = int(stddraw.mouseX() // 20)
                        y = int((stddraw.mouseY() - 10) // 20)
                        possible_matches = check_matches(board, select, (x, y))
                        if ((y == select[1] and (x == select[0] - 1 or x == select[0] + 1)) or (x == select[0] and (y == select[1] - 1 or y == select[1] + 1))) and len(possible_matches) != 0:
                            board = switch(board, select, (x, y))
                            select = None
                            matches = possible_matches
                            moves -= 1
                            anim_counter = 5
                        else:
                            select = None
                    else:
                        select = None

        for i in range(7):
            shift = False
            if i in shifts.keys():
                shift = True
            for k in range(9):
                if board[i][k] != 0:
                    x = i * 20
                    y = k * 20 + 10
                    trans = 0
                    if shift:
                        if k >= shifts[i]:
                            trans = anim_counter * 4
                    match = False
                    if (i, k) in matches:
                        match = True
                    if board[i][k] == 1:
                        draw_circle(x, y + trans, match)
                    elif board[i][k] == 2:
                        draw_square(x, y + trans, match)
                    elif board[i][k] == 3:
                        draw_triangle(x, y + trans, match)
                    elif board[i][k] == 4:
                        draw_diamond(x, y + trans, match)
                    elif board[i][k] == 5:
                        draw_para(x, y + trans, match)
                    elif board[i][k] == 6:
                        draw_pentagon(x, y + trans, match)
        stddraw.setPenColor(stddraw.color.WHITE)
        if select is not None:
            draw_selector(select)
        stddraw.text(35, 5, 'Score: ' + str(score))
        stddraw.text(105, 5, f'Moves Remaining: ' + str(moves))
    stddraw.show(30)