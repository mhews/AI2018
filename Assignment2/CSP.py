import sys
import copy
import numpy as np
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
maze = open('8x8maze.txt', 'r')
printer = open('solution.txt','w')
solution = []
endpoint = []
for line in maze:
    row = []
    for i in line:
        row.append(i)
        if i != '_' and i != '\n':
            endpoint.append (Node(i, len(solution), len(row) - 1))
    solution.append(row)
solution = np.array(solution)


def choices(x, y, color, sol):
    #find all possible moves or return 0 if adjacent to end
    localDomain = []
    if x + 1 < len(sol):
        check = sol[x + 1][y]
        if check == '_':
            localDomain.append((x + 1, y))
        elif check == color:
            return 0
    if x - 1 >= 0:
        check = sol[x - 1][y]
        if check == '_':
            localDomain.append((x - 1, y))
        elif check == color:
            return 0
    if y + 1 < len(sol):
        check = sol[x][y + 1]
        if check == '_':
            localDomain.append((x, y + 1))
        elif check == color:
            return 0
    if y - 1 >= 0:
        check = sol[x][y - 1]
        if check == '_':
            localDomain.append((x, y - 1))
        elif check == color:
            return 0


    return localDomain
def output(sol):
    for line in sol:
        for i in line:
            printer.write(i.upper())
    printer.close()

def solve (sol, endpoint):
    btDecisions = None
    branches = []
    while (len(endpoint) > 0):
        removes = []
        for ep in endpoint:#find list of possible moves for each endpoint
            check = (choices (ep.x, ep.y, ep.color, sol))
            if check == 0:#remove endpoint if it connects to compliment endpoint
                removes.append(ep)

            elif len(check) == 0:#backtrack if an endpoint has nowhere else to go
                backtrack = branches.pop()
                sol = backtrack.state
                endpoint = backtrack.endpoints
                btDecisions = backtrack.decisions
                break
            else:
                ep.addchoices(check)
            if len(endpoint) - len(removes) == 0: #all endpoints matched
                output(sol)
                sys.exit(0)
        for r in removes:
            endpoint.remove(r)
        endpoint.sort(key=lambda x: len(x.choice), reverse=False) #sort endpoints by number of options
        index = 0
        newState = endpoint[0]#endpoint with least possible moves
        if btDecisions: #handle backtracked state
            ch = btDecisions[0]
            if len(btDecisions) > 1:
                branches.append(Branch(copy.deepcopy(sol), copy.deepcopy(endpoint), btDecisions[1:]))
            btDecisions = None
        else:
            ch = newState.choice[0] #first possible move for endpoint
        if len(newState.choice) > 1: #store current state of game and all endpoints as a separate branch for additional possible moves
            branches.append(Branch(copy.deepcopy(sol), copy.deepcopy(endpoint), newState.choice[1:]))
        sol[ch[0]][ch[1]] = newState.color #edit game
        sol[newState.x][newState.y] = newState.color.lower()
        del endpoint[0] #move endpoint
        endpoint.append(Node(newState.color, ch[0], ch[1]))



solve(solution, endpoint)
