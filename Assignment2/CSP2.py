import sys
import copy
import numpy as np
import time

start = time.time()
class Node:
    choice = []
    def __init__(this, color, x, y):
        this.color = color
        this.x = x
        this.y = y
    def addchoices(this, choices):
        this.choice = choices

class Branch:
    def __init__(this, state, endpoints, decisions):
        this.state = state
        this.endpoints = endpoints
        this.decisions = decisions
maze = open('10x10maze.txt', 'r')
printer = open('solution.txt','w')
solution = []
endpoint = []
for line in maze:
    row = []
    for i in line:
        if (i != '\n' and i != ' '):
            row.append(i)
            if i != '_':
                endpoint.append (Node(i, len(solution), len(row) - 1))
    if len(row) > 0:
        solution.append(row)
solution = np.array(solution)
solution.resize([10,10])

def choices(x, y, color, sol):
    #find all possible moves or return 0 if adjacent to end
    localDomain = []
    same_colors = 0
    if x + 1 < len(sol):
        check = sol[x + 1][y]
        if check == '_':
            localDomain.append((x + 1, y))
        elif check == color:
            return 0
        elif check == color.lower():
            same_colors += 1
    if x - 1 >= 0:
        check = sol[x - 1][y]
        if check == '_':
            localDomain.append((x - 1, y))
        elif check == color:
            return 0
        elif check == color.lower():
            same_colors += 1
    if y + 1 < len(sol):
        check = sol[x][y + 1]
        if check == '_':
            localDomain.append((x, y + 1))
        elif check == color:
            return 0
        elif check == color.lower():
            same_colors += 1
    if y - 1 >= 0:
        check = sol[x][y - 1]
        if check == '_':
            localDomain.append((x, y - 1))
        elif check == color:
            return 0
        elif check == color.lower():
            same_colors += 1
    if same_colors >= 2:
        return []

    return localDomain

def Test(solu, ep1, ep2, color):
    frontier = [ep1]
    solu[ep1[0]][ep1[1]] = '#'
    while len(frontier) > 0:
        curPos = frontier.pop()
        check = choices(curPos[0], curPos[1], color, solu)

        distance = 100
        if check == 0:
            return True
        elif len(check) == 0:
            continue
        elif len(check) == 1:

            frontier += check
        else:
            for ch in check:
                new_dist = abs(ch[0] - ep2.y) + abs(ch[1] - ep2.x)
                if new_dist < distance:
                    distance = new_dist
                    temp = ch
                    check.remove(ch)
                    check.insert(0,temp)

            frontier += check
        for ch in check:
            solu[ch[0]][ch[1]] = '#'
    return False
    
def output(sol):
    for line in sol:
        for i in line:
            printer.write(i.upper())
        printer.write('\n')
    end = time.time()
    printer.write(str(end - start))
    printer.close()

def complete(sol): #all spaces are filled
    for line in sol:
        for i in line:
            if i == '_':
                return False
    return True

def solve (sol, endpoint):
    removes = []
    for ep in endpoint:#find list of possible moves for each endpoint
        check = (choices (ep.x, ep.y, ep.color, sol))
        if check == 0:#remove endpoint if it connects to compliment endpoint
            removes.append(ep)
        elif len(check) == 0:#backtrack if an endpoint has nowhere else to go
            return 0
        else:
            ep.addchoices(check)
        if len(endpoint) - len(removes) == 0: #all endpoints matched
            if complete(sol):
                output(sol)
                sys.exit(0)
            else:
                return 0
    for r in removes:
        endpoint.remove(r)
    endpoint.sort(key=lambda x: len(x.choice), reverse=False) #sort endpoints by number of options
    index = 0
    for state in endpoint[0].choice:
        tempep = copy.deepcopy(endpoint)

        tempsol = copy.deepcopy(sol)
        tempsol[state[0]][state[1]] = endpoint[0].color #edit game
        tempsol[endpoint[0].x][endpoint[0].y] = endpoint[0].color.lower()
        del tempep[0] #move endpoint
        tempep.insert(0, Node(endpoint[0].color, state[0], state[1]))
        valid = True
        for i in range(len(tempep) - 1):
            endpoint2 = 0
            for x in tempep[i + 1:]:
                if x.color == tempep[i].color:

                    endpoint2 = x
            if endpoint2 != 0:
                if not Test(copy.deepcopy(tempsol), (tempep[i].x, tempep[i].y), endpoint2, endpoint2.color):
                    valid = False
                    break
        if valid:
            solve(tempsol, tempep)
        index += 1

solve(solution, endpoint)
