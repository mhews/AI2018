
from pprint import pprint
import time
import sys
import random
import math

# Constants
MAZE = "../5x5maze.txt"
BLANK = "_"
DUMB = True
SMART = False
TERM = '$'

# Public Functions
def zeroArr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = '0'


class DumbSolver:


    def __init__(self):

        # Gather a list of values for this problem
        self.constraints = []
        # All of the constraint values and the tuple of constraint values on
        # the end points. Determine the most constrained on both ends.
        self.cValues = {}
        # Board stack for visiting order; one stack for each value. List of 
        #    lists for each values movement stack. Will be one for one with 
        #    constraints[]. Bottom of stack is $.
        self.sNodes = []
        self.board = Board()

        # --------------  END __init__()   --------------------------- #


    def find_path_heads(self):
        for row in self.board.arr:
            for element in row:
                if element.iData != BLANK and element.iData != None:
                    if element.iData not in self.cValues:
                        self.cValues[element.iData] = []


    def add_constraints(self):
        for row in self.board.arr:
            for element in row:
                if element.iData != BLANK and element.iData != None:
                    if element.iData not in self.constraints:
                        self.constraints.append(element.iData)
        self.sNodes = [['$'] for element in self.constraints]


    def printArr(self):
        self.board.printArr()

    def populate_startConstraints(self):
        for i in range(len(self.board.arr)):
            for j in range(len(self.board.arr[0])):
                # Get all of the values with one pass and check against valid
                #    constraints[]
                if self.board.arr[i][j].iData != BLANK and self.board.arr[i][j].iData != None \
                                and self.board.arr[i][j].iData in self.constraints:
                    # return a list
                    #x = self.calc_constraintVal(element)
                    self.cValues[self.board.arr[i][j].iData] \
                                        .append(self.calc_constraintVal(i, j) )


    def calc_constraintVal(self, i, j):
        # Look up, down, right and left
        constraintVal = 0
        if (i < len(self.board.arr) - 1) and (self.board.arr[i + 1][j] \
                    .iData == BLANK or self.board.arr[i + 1][j].iData == None):
            constraintVal += 1
        if i > 1 and (self.board.arr[i - 1][j].iData == BLANK or self \
                                        .board.arr[i - 1][j].iData == None):
            constraintVal += 1
        if (j < len(self.board.arr[0]) - 1) and (self.board.arr[i][j + 1] \
                    .iData == BLANK or self.board.arr[i][j + 1].iData == None):
            constraintVal += 1
        if j > 0 and (self.board.arr[i][j - 1].iData == BLANK \
                                or self.board.arr[i][j - 1].iData == None):
            constraintVal += 1
        return constraintVal

    def is_empty(self, struct):
        if struct:
            return False
        else:
            return True

    def order_cValues(self):
        # clear constraints
        self.constraints = []
        lConstraints= {}
        # Use Cvals to order them. The stack will be one-to-one with this list.
        for key in self.cValues:
            lConstraints[key] = sum(self.cValues[key])
        while not self.is_empty(lConstraints):
            for key in lConstraints:
                low = min(lConstraints, key=lConstraints.get)
            self.constraints.append(low)
            lConstraints.pop(low)

    def nLocate(self, val):
        # This will return the first element with a particular value that 
        # is found.
        for i in range(len(self.board.arr)):
            for j in range(len(self.board.arr[0])):
                if self.board.arr[i][j].iData == val:
                    return i, j

    def place_path(self, path, color):
        if not path:
            return False
        for element in path:
            if self.board.arr[element[0]][element[1]].nColor == None:
                self.board.arr[element[0]][element[1]].nColor = color
            elif self.board.arr[element[0]][element[1]].nColor == color:
                continue
            else:
                print("Error placing path.")
                print("color = %r" % color)
                print("nColor = %r" % self.board.arr[element[0]][element[1]].nColor)
                self.printArr()
                return False
        self.printArr()
        return True

    def remove_symbol(self, symbol):
        # Remove this symbol from the graph
        for row in self.board.arr:
            for element in row:
                if element.nColor == symbol and element.iData != element.nColor:
                    element.nColor = None
                if symbol in element.nMarked:
                    element.nMarked.remove(symbol)


    def elementRewind_h(self, element, curPos, targetSymbol):
        # Look up, down, left, right until we've found the same marked symbol.
        # Then ask yourself, is the element touching me?
        # DOWN
        u = curPos[0]
        v = curPos[1]
        lUP = False
        lDOWN = False
        lLEFT = False
        lRIGHT = False
        returnIt = False
        # Look up, down, left, right for element and if it's adjacent continue
        #    taking element as the next move.
        # check if any of these directions are going to be out of bounds
        # We're in the center of the board. Go forth and conquer
        #if self.board.arr[curPos[0]][curPos[1]].nColor == targetSymbol:
            #self.board.arr[curPos[0]][curPos[1]].nColor = None
            #self.board.arr[curPos[0]][curPos[1]].nMarked.remove(targetSymbol)

        if u < len(self.board.arr) - 1:
            lDOWN = True
        if u > 0:
            lUP = True
        if v > 0:
            lLEFT = True
        if v < len(self.board.arr[0]) - 1:
            lRIGHT = True

        if self.board.arr[curPos[0]][curPos[1]].mChoice:
            if lDOWN:
                #Down
                if u + 1 == element[0]:
                    returnIt = True
            if lUP:
                # UP
                if u - 1 == element[0]:
                    returnIt = True
            if lRIGHT:
                # Right
                if v + 1 == element[1]:
                    returnIt = True
            if lLEFT:
                # Left
                if v - 1 == element[1]:
                    returnIt = True

        if returnIt:
            # We've found the adjacent node, continue from here
            return curPos
            
        if lDOWN:
            # Down
            if self.board.arr[u + 1][v].nColor == targetSymbol \
                                            and targetSymbol in self.board.arr[u + 1][v].nMarked:
                # This is then next position to move to.
                    self.board.arr[curPos[0]][curPos[1]].nColor = None
                    self.board.arr[curPos[0]][curPos[1]].nMarked.remove(targetSymbol)
                    return self.elementRewind_h(element, (u + 1, v), targetSymbol)
        if lUP:
            # UP
            if self.board.arr[u - 1][v].nColor == targetSymbol and targetSymbol \
                                            in self.board.arr[u - 1][v].nMarked:
                    self.board.arr[curPos[0]][curPos[1]].nColor = None
                    self.board.arr[curPos[0]][curPos[1]].nMarked.remove(targetSymbol)
                    return self.elementRewind_h(element, (u - 1, v), targetSymbol)
        if lLEFT:
            # LEFT
            if self.board.arr[u][v - 1].nColor == targetSymbol and targetSymbol \
                                        in self.board.arr[u][v - 1].nMarked:
                    self.board.arr[curPos[0]][curPos[1]].nColor = None
                    self.board.arr[curPos[0]][curPos[1]].nMarked.remove(targetSymbol)
                    return self.elementRewind_h(element, (u, v - 1), targetSymbol)
        if lRIGHT:
            # RIGHT
            if self.board.arr[u][v + 1].nColor == targetSymbol and targetSymbol in \
                                                    self.board.arr[u][v + 1].nMarked:
                    self.board.arr[curPos[0]][curPos[1]].nColor = None
                    self.board.arr[curPos[0]][curPos[1]].nMarked.remove(targetSymbol)
                    return self.elementRewind_h(element, (u, v + 1), targetSymbol)

    # --------------------- END elementRewind_h() ---------------------------- #


    def elementRewind(self, element, symbol, path):
        # Rewind the path with the symbol to the state where the element was a choice
        if not path:
            # This means we're dealing with a finished path. Look for end element.
            for u in range(len(self.board.arr)):
                for v in range(len(self.board.arr[0])):
                    if self.board.arr[u][v].iData == symbol and self.board.arr[u][v] \
                                        .iData == self.board.arr[u][v].nColor and \
                                        symbol not in self.board.arr[u][v].nMarked:
                        # found the tail and we can call the recursive function passing in the
                        #     tail of the path.

                         # Down
                        if u < len(self.board.arr) - 1 and self.board.arr[u + 1][v].nColor == symbol \
                                                    and symbol in self.board.arr[u + 1][v].nMarked:
                            return self.elementRewind_h(element, (u + 1, v), symbol)
                        # UP
                        if u > 0 and  self.board.arr[u - 1][v].nColor == symbol and symbol \
                                                    in self.board.arr[u - 1][v].nMarked:
                            return self.elementRewind_h(element, (u - 1, v), symbol)
                        # LEFT
                        if v > 0 and self.board.arr[u][v - 1].nColor == symbol and symbol \
                                                    in self.board.arr[u][v - 1].nMarked:
                            return self.elementRewind_h(element, (u, v - 1), symbol)
                        # RIGHT
                        if v < len(self.board.arr[0]) - 1 and self.board.arr[u][v + 1] \
                                                .nColor == symbol and symbol in self.board \
                                                                    .arr[u][v + 1].nMarked:
                            return self.elementRewind_h(element, (u, v + 1), symbol)

        else:
            pass


    def backPropagate(self, symbol, path):
        # Record state

        lStack_idx = self.constraints.index(symbol)

        while True:
            self.printArr()
            if self.sNodes[lStack_idx][(len(self.sNodes[lStack_idx]) - 1)] != TERM:
                element_rwnd = self.sNodes[lStack_idx].pop(len(self.sNodes[lStack_idx]) - 1)
                continueNode = self.elementRewind(element_rwnd, self.constraints[lStack_idx], path)
                break
            else:
                # get rid this symbol
                self.remove_symbol(self.constraints[lStack_idx])
                lStack_idx -= 1
                symbol = self.constraints[lStack_idx]
            self.printArr()
        # Pop stack lifo. For all (x, y) remove path nodes | (x, y) is in moves.
        # continue until symbol stack is empty.
        return continueNode

        # Remove traces of symbol before continuing with symbol-1 in global stack.

        # continue until stack is empty: Error || symbol path has been completed.

        # make sure stack is complete through symbol when returning control.


    # -------------- END backPropogate() ------------------ #

    def solveit(self):
        if DUMB:
            # Order the nodes from most constrained to least constrained.
            self.order_cValues()
            # Init DFS
            dfs = DFS(self.board.arr, self.sNodes, self.constraints)
            # elements are ordered and ready to find path
            for element in self.constraints:
                i, j = self.nLocate(element)
                if not dfs.set_target(i, j):
                    print("1100001")
                    sys.exit(1)
                iPath = dfs.dfs_search(i, j)
                if len(iPath) > 0:
                    iPath.append((i, j))
                if not self.place_path(iPath, element):
                    cNode = self.backPropagate(element, iPath)
                    print("\n")

        if SMART:
            pass



    # -------------- END solveit() --------------- #

#end class DumbSolver


class Board:

    def __init__(self):
        # The environment
        self.arr = None
        # Read in the env.
        with open(MAZE, "r") as file:
            self.arr = [[Node(n) for n in line if n != '\n']
                         for line in file if line != '\n']


    def printArr(self):
        for row in self.arr:
            for element in row:
                if element.iData != None or element.nColor != None:
                    print(element.nColor, end=" ")
                elif (element.iData == None or element.iData == BLANK):
                    print(BLANK, end=" ")
            print(end="\n")
        print("\n")


# END class Board



class Node:


    def __init__(self, dataIn):
        # The value for a particular element on the grid.
        if dataIn == BLANK:
            # perminant starting mark
            self.iData = None
            # a node that does not have a starting value and can be
            # changed.
            self.nColor = None
        else:
            self.iData = dataIn
            self.nColor = dataIn
        # Numerical value denoting restrictions on a node.
        self.restrictions = None
        # list of possible values for a variable.
        self.pValues = []
        # Did I make a choice and put one on the stack?
        self.mChoice = False
        # A list of visits
        self.nMarked = []

#end class Node

    def mark_node(self, mark):
        if mark not in self.nMarked and (self.nColor == None or self.nColor == mark):
            self.nMarked.append(mark)
            return True

        else:
            return False


    def pop_color(self, color):
        if self.nColor == color:
            self.nColor = None
            return True
        else:
            return False



class DFS:

    def __init__(self, iGraph, gStack, gStack_order):
        # The input graph
        self.iGraph = iGraph
        self.target = None
        # the graph stack, contains all of the stacks for the particular graph
        self.gStack = gStack
        self.gStack_order = gStack_order


    def set_target(self, i, j):
        self.target = self.iGraph[i][j].iData
        if self.target in self.gStack_order:
            return True
        else:
            print("Something went wrong setting the target node.")
            return False



    # Given a graph and a position containing some node's data. Search for
    #    the data element and return a sequence of nodes representing the path from
    #     in position to out position.
    def dfs_search(self, iItr, jItr):

        # check if any fo the next moves is a target. If so, pick it. If not,
        # pick something else and return it. Return the next move in idx 0. The rest
        # to be pushed onto stack in the trailing positions.
        path = []
        lNext_Position = self.check_directions(iItr, jItr)
        if len(lNext_Position) > 0:
            while len(lNext_Position) > 0:
                if len(lNext_Position) == 1:
                    i = lNext_Position[0][0]
                    j = lNext_Position[0][1]
                    lNext_Position = []
                else:
                    # Push the end to the stack
                    tempPos = lNext_Position.pop(len(lNext_Position) - 1)
                    tempIndex = self.gStack_order.index(self.target)
                    self.gStack[tempIndex].append(tempPos)
                    self.iGraph[iItr][jItr].mChoice = True
            
            if not self.iGraph[iItr][jItr].mark_node(self.iGraph[iItr][jItr].iData):
                print("Could not mark the node.")
                print("1300001")
                sys.exit(1)

            path = self.dfs_helper(i, j)
            return path
        return path


        # -------------- END dfs_search() ---------------------- #
    # recursive helper function, 
    # POST: Return a list of nodes corresponding to the path from start to
    #       end element.
    def dfs_helper(self, iItr, jItr):

        if self.iGraph[iItr][jItr].iData == self.target:
            return [(iItr, jItr)]

        lNext_Position = self.check_directions(iItr, jItr)
        # Remove the possibilities that have been visited
        flag = False
        for element in lNext_Position:
            if self.iGraph[element[0]][element[1]].iData == self.target:
                i = element[0]
                j = element[1]
                flag = True
        if not flag:
            lNext_Position = self.cleanPosition(lNext_Position)

            while len(lNext_Position) > 0:
                if len(lNext_Position) == 1:
                    i = lNext_Position[0][0]
                    j = lNext_Position[0][1]
                    lNext_Position = []
                else:
                    # Push the end to the stack
                    tempPos = lNext_Position.pop(len(lNext_Position) - 1)
                    tempIndex = self.gStack_order.index(self.target)
                    self.gStack[tempIndex].append(tempPos)
                    self.iGraph[iItr][jItr].mChoice = True

        if not self.iGraph[iItr][jItr].mark_node(self.target):
            print("Could not mark the node.")
            print("1355501")
            sys.exit(1)

            #print("Stop")

        lPath = self.dfs_helper(i, j)
        lPath.append((iItr, jItr))
        return lPath


    # --------------------- END dfs_search() ----------------------- #

    def check_directions(self, i, j):
        lDirections = []
        if (i < len(self.iGraph) - 1) and (self.iGraph[i + 1][j].iData == None \
                            or self.iGraph[i + 1][j].iData == self.target) and \
                            self.target not in self.iGraph[i + 1][j].nMarked and \
                            (self.iGraph[i + 1][j].nColor == None or self.iGraph[i + 1][j].nColor == self.target):
            lDirections.append((i + 1, j))
        if i > 1 and (self.iGraph[i - 1][j].iData == None or self.iGraph[i - 1][j] \
                                        .iData == self.target) and self.target \
                                        not in self.iGraph[i - 1][j].nMarked and \
                                        (self.iGraph[i - 1][j].nColor == None or self.iGraph[i - 1][j].nColor == self.target):
            lDirections.append((i - 1, j))
        if (j < len(self.iGraph[0]) - 1) and (self.iGraph[i][j + 1].iData == None \
                            or self.iGraph[i][j + 1].iData == self.target) \
                            and self.target not in self.iGraph[i][j + 1].nMarked and \
                            (self.iGraph[i][j + 1].nColor == None or self.iGraph[i][j + 1].nColor == self.target):
            lDirections.append((i, j + 1))
        if j > 0 and (self.iGraph[i][j - 1].iData == None or self.iGraph[i][j - 1] \
                                        .iData == self.target) and self.target \
                                        not in self.iGraph[i][j - 1].nMarked and \
                                        (self.iGraph[i][j - 1].nColor == None or self.iGraph[i][j - 1].nColor == self.target):
            lDirections.append((i, j - 1))

        return lDirections

    def cleanPosition(self, list):
        if len(list) == 0:
            print("No next position; list is empty.")
            print("1700001")
            sys.exit(1)
        elif len(list) == 1:
            if self.target in self.iGraph[list[0][0]][list[0][1]].nMarked and \
                     (self.iGraph[list[0][0]][list[0][1]].iData != None and \
                     self.iGraph[list[0][0]][list[0][1]].iData != BLANK):
                print("Only one position and it is marked.")
                print("1705001")
                sys.exit(1)
            else:
                return list
        else:
            tList = []
            while len(list) > 0:
                if self.target not in self.iGraph[list[0][0]][list[0][1]].nMarked and \
                            (self.iGraph[list[0][0]][list[0][1]].iData != None or \
                            self.iGraph[list[0][0]][list[0][1]].iData != BLANK):
                    tList.append(list[0])
                    list.pop(0)
                else:
                    list.pop(0)
            return tList
        print("1706001")
        sys.exit(1)

#end class DFS


def main():
    dummy = DumbSolver()
    dummy.find_path_heads()
    dummy.add_constraints()
    dummy.populate_startConstraints()
    dummy.printArr()
    dummy.solveit()

    time.sleep(1)
if __name__ == "__main__": main()


