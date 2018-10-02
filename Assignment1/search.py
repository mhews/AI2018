

file = open('medium maze.txt', 'r')
solution = open('solution.txt', 'w')

maze = []
goal = None


class location():
#class containing points, x coordinate, y coordinate, and point connecting to it
    def __init__(self, x, y, previous):
        self.previous = previous
        self.x = x
        self.y = y

#reading in file to 2D array
for line in file:
    row = []
    for symbol in line:
        row += symbol
        if (symbol == 'P'):
            #starting location
            frontier = [location(len(maze),len(row) - 1, None)]
        if (symbol == '*'):
            #goal
            goal = location(len(maze), len(row) - 1, None)
    maze.append(row)


#return whether it can move in direction
def down(maze, loc):
    if maze[loc.x][loc.y + 1] == ' ':
        maze[loc.x][loc.y + 1] = 'X' #we have been to this point
        return 1
    elif maze[loc.x][loc.y + 1] == '*':
        return 2
    else:
        return 0

def up(maze, loc):
    if maze[loc.x][loc.y - 1] == ' ':
        maze[loc.x][loc.y - 1] = 'X'
        return 1
    elif maze[loc.x][loc.y - 1] == '*':
        return 2
    else:
        return 0

def left(maze, loc):
    if maze[loc.x - 1][loc.y] == ' ':
        maze[loc.x - 1][loc.y] = 'X'
        return 1
    elif maze[loc.x - 1][loc.y] == '*':
        return 2
    else:
        return 0

def right(maze, loc):
    if maze[loc.x + 1][loc.y] == ' ':
        maze[loc.x + 1][loc.y] = 'X'
        return 1
    elif maze[loc.x + 1][loc.y] == '*':
        return 2
    else:
        return 0
    
def possibleMoves(maze, temp):
    #adds all possible moves to the frontier
    frontier = []
    loc = location(temp.x, temp.y, temp.previous)
    test = down(maze, loc)
    if test == 1:
        frontier.append (location(loc.x,loc.y + 1, temp))
    elif test == 2:
        return 1
    test = up(maze, loc)
    if test == 1:
        frontier.append(location(loc.x,loc.y - 1, temp))
    elif test == 2:
        return 1
    test = left(maze,loc)
    if test == 1:
        frontier.append(location(loc.x - 1, loc.y, temp))
    elif test == 2:
        return 1
    test = right(maze, loc)
    if test == 1:
        frontier.append (location(loc.x + 1, loc.y, temp))
    elif test == 2:
        return 1
    return frontier


def output():
    #write maze to file
    for row in maze:
        for i in row:
            if (i == 'X'):
                solution.write(' ')
            else:
                solution.write (i)

def DFS(maze, frontier):
    #depth first
    expanded = 0
    while len(frontier) > 0:
        loc = frontier.pop() #pop from top of stack
        pm = possibleMoves(maze,loc) #return local frontier for current node
        if pm == 1:
            break
        expanded += len(pm) #add possible moves to total expanded nodes
        frontier = frontier + pm #add possible moves to top of frontier stack


    while not loc.previous == None:
        maze[loc.x][loc.y] = '.'
        loc = loc.previous
    output()
    solution.write('\n' + str(expanded))

def BFS(maze, frontier):
    expanded = 0;

    while len(frontier) > 0:
        loc = frontier.pop(0) #take from front of queue
        pm = possibleMoves(maze,loc)
        if pm == 1:
            break
        expanded += len(pm)
        frontier = frontier + pm

    while not loc.previous == None:
        maze[loc.x][loc.y] = '.'
        loc = loc.previous
    output()
    solution.write('\n' + str(expanded))
    
def distance(loc):
    # No need take sqrt. gives the same relative info.
    distance_toGoal = (loc.x - goal.x)**2 + (loc.y - goal.y)**2
    return distance_toGoal
    
def GREEDY(maze, frontier):
    # if possibleMoves() returns 1, that means it's a goal state.
    #     otherwise, it will return a list of locations to check.
    expanded = 0
    while len(frontier) > 0:
        # frontier.sort(key=None, reverse=False)
        loc = frontier.pop(0)
        pm = possibleMoves(maze, loc)
        i_dist = None
        next_move = None
        next_move_dist = None
        if pm == 1:
            break
        for i in pm: 
            i_dist = distance(i)
            if next_move_dist is None:
                next_move_dist = i_dist
                next_move = i
            elif i_dist < next_move_dist:
                next_move_dist = i_dist
                next_move = i
        expanded += 1
        frontier.append(next_move)
    while not loc.previous == None:
        maze[loc.x][loc.y] = '.'
        loc = loc.previous
    output()
    solution.write('\n' + str(expanded))
    
    
GREEDY(maze, frontier)


solution.close()
