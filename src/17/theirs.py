import re

def q17_parse(s):
    l = s.splitlines()
    board = []
    vl = []
    for e in l:
        xg = [int(k) for k in re.search(r"x=(\d+)(?:\.\.(\d+))?",e).groups() if k != None]
        yg = [int(k) for k in re.search(r"y=(\d+)(?:\.\.(\d+))?",e).groups() if k != None]
        if len(xg) == 1:
            xg = xg + xg
        if len(yg) == 1:
            yg = yg + yg
        v = tuple(sorted(xg) + sorted(yg))
        vl.append(v)
    minx = min([v[0] for v in vl]) - 1
    maxx = max([v[1] for v in vl]) + 1
    miny = min([v[2] for v in vl])
    maxy = max([v[3] for v in vl])
    xw = maxx - minx + 1
    yw = maxy - miny + 1
    board = [[" "] * xw for _ in range(yw)]
    for v in vl:
        for x in range(v[0],v[1]+1):
            for y in range(v[2],v[3]+1):
                board[y-miny][x-minx] = "#"
    
    return board,minx

def testdown(board,x,y):
    return (y+1 >= len(board) or board[y+1][x] in [" ","*",">"])

def testleft(board,x,y):
    return (board[y][x-1] in [" ","*",">"])

def testright(board,x,y):
    return (board[y][x+1] in [" ","*",">"])

def touch_with_water(board,x,y,water):
    if board[y][x] == " ":
        board[y][x] = "*"
        water += 1
    return board,water
    
def q17board(s):
    board,minx = q17_parse(s)
    for r in board:
        print("".join(r))

def q17b(s):
    board,minx = q17_parse(s)
    board0 = board[:]
    yw = len(board)
    spoutx = 500 - minx
    t = 0
    lastwater = 0
    water = 0
    # work out where the 
    intersections = [(spoutx,0)]
    while True:
        x,y = intersections[-1]
        while True:
            #   = untouched, * = touched, # = wall, = = full
            if y >= len(board):
                break
            board,water = touch_with_water(board,x,y,water)
            # test down
            if testdown(board,x,y):
                # move down, leaving only a *
                y += 1
                continue
            else:
                if (board[y][x-1] == "#") and (board[y][x+1] == "#"):
                    board[y][x] = "="
                    y -= 1
                    continue
                # test left
                xl = x
                xr = x
                if board[y][x] != ">":
                    while testleft(board,x,y):
                        x -= 1
                        xl -= 1
                        board,water = touch_with_water(board,x,y,water)
                        if testdown(board,x,y):
                            break
                    if testdown(board,x,y):
                        # mark the point to see if we need to check the right-hand side
                        if (xr,y) not in intersections:
                            intersections.append((xr,y))
                        y += 1
                        continue
                    x = xr
                # test right
                while testright(board,x,y):
                    x += 1
                    xr += 1
                    board,water = touch_with_water(board,x,y,water)
                    if testdown(board,x,y):
                        break
                if testdown(board,x,y):
                    y += 1
                    continue
                # we've hit walls on both sides, fill them up
                if board[y][xl-1] == "#" and board[y][xr+1] == "#":             
                    for xx in range(xl,xr+1):
                        board[y][xx] = "="
                break
        if lastwater == water:
            if len(intersections) == 1:
                # verify
                check = 0
                for y in range(len(board0)):
                    for x in range(len(board0[0])):
                        if board0[y][x] == "#":
                            assert(board[y][x] == "#")
                        else:
                            assert(board[y][x] != "#")
                for r in board:
                    for k in r:
                        if k not in ['#', ' ']:
                            check += 1
                    print("".join(r))
                return check
            else:
                x,y = intersections.pop()
                # print(intersections)
                if board[y][x] == "*":
                    intersections.append((x,y))
                    board[y][x] = ">"
        lastwater = water

check = q17b(open('./input/input.dat').read())
print(check)
