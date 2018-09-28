file = open('open maze.txt', 'r')
solution = open('solution.txt', 'w')

maze = []

class location():

    def __init__(self, x, y, previous):
        self.previous = previous
        self.x = x
        self.y = y

for line in file:
    row = []
    for symbol in line:
        row += symbol
        if (symbol == 'P'):
            frontier = [location(len(maze),len(row) - 1, None)]
    maze.append(row)



def down(maze, loc):
    if maze[loc.x][loc.y + 1] == ' ':
        return 1
    elif maze[loc.x][loc.y + 1] == '*':
        return 2
    else:
        return 0

def up(maze, loc):
    if maze[loc.x][loc.y - 1] == ' ':
        return 1
    elif maze[loc.x][loc.y - 1] == '*':
        return 2
    else:
        return 0

def left(maze, loc):
    if maze[loc.x - 1][loc.y] == ' ':
        return 1
    elif maze[loc.x - 1][loc.y] == '*':
        return 2
    else:
        return 0

def right(maze, loc):
    if maze[loc.x + 1][loc.y] == ' ':
        return 1
    elif maze[loc.x + 1][loc.y] == '*':
        return 2
    else:
        return 0
def possibleMoves(maze, temp):
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
    if not maze[loc.x][loc.y] == 'P':
        maze[loc.x][loc.y] = 'X'
    return frontier
def output():
    for row in maze:
        for i in row:
            if (i == 'X'):
                solution.write(' ')
            else:
                solution.write (i)
def DFS(maze, frontier):
    expanded = 0
    while len(frontier) > 0:
        loc = frontier.pop()
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

def BFS(maze, frontier):
    expanded = 0;

    while len(frontier) > 0:
        loc = frontier.pop(0)
        pm = possibleMoves(maze,loc)
        if pm == 1:
            break
        expanded += len(pm)
        frontier = frontier + pm
        if not maze[loc.x][loc.y] == 'P':
            maze[loc.x][loc.y] = 'X'

    while not loc.previous == None:
        maze[loc.x][loc.y] = '.'
        loc = loc.previous
    output()
    solution.write('\n' + str(expanded))
DFS(maze, frontier)


solution.close()
