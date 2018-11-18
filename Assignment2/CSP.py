class Node:
    def __init__(this, color, previous):
        this.color = color
        this.previous = previous
        this.path = False

maze = open('5x5maze.txt', 'r')
output = open('solution.txt','w')
domain = []
solution = []
endpoint = []
for line in maze:
    row = []
    for i in line:
        row.append(Node(i, False))
        if i != '_' and i != '\n':
            row[-1].path = True
            domain.append ((len(solution), len(row) - 1))
    solution.append(row)
domain = list(set(domain))

def choices(x, y):
    localDomain = []
    for i in [-1,1]:
        try:
            if solution[x + i][y] != '\n' and not solution[x + i][y].path and solution[x + i][y].color !=  solution[x][y].color:
                localDomain.append((x + i, y))
                solution[x + i][y].color = solution[x][y].color
            elif solution[x + i][y].previous == None and solution[x + i][y].color == solution[x][y].color:
                return 0
        except:
            continue
        try:
            if solution[x][y + i] != '\n' and not solution[x][y + i].path and solution[x][y + i].color !=  solution[x][y].color:
                localDomain.append((x, y + i))
                solution[x][y + i].color = solution[x][y].color
            elif solution[x][y + i].previous == None and solution[x][y + i].color == solution[x][y].color:
                return 0
        except:
            continue
    return localDomain
path = []
currentColor = None
while len(domain) != 0:
    x = domain.pop()
    if solution[x[0]][x[1]].color != currentColor:
        for i  in path:
            if i.color == solution[x[0]][x[1]].color:
                i.path = False
    currentColor = solution[x[0]][x[1]].color
    check = choices(x[0],x[1])
    if choices == 0:
        x = solution[x[0]][x[1]]
        while x.previous != None:
            x.path = True
            path += x
            x.color = '_'
            x = x.previous
        x = domain.pop(0)
        if solution[x[0]][x[1]].path:
            break
        domain += x
    else:
        domain += check


for line in solution:
    for i in line:
        output.write(i.color)
    output.write('\n')
output.close()
