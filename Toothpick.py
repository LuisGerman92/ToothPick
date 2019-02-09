# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:28:54 2019

@author: Luis G

Toothpick

Generates a list of pairs of points that can be used to draw the toothpick curve.
"""
# indices used as constants
X = 0
Y = 1
RIGHT = 0
LEFT  = 1

# Iterations for the program
MAX_ITERATIONS = 5
# current iteration
n = 1

# debug levels
DEBUG   = 10
INFO    = 20
WARNING = 30
ERROR   = 40
FAILURE = 60
# Set the appropriate logging level
LOGLEVEL = INFO

def log(level, message):
    if level >= LOGLEVEL:
        if(level == DEBUG):
            str1 = "[DEBUG] "
        if(level == INFO):
            str1 = "[INFO] "
        if(level == WARNING):
            str1 = "[WARNING] "
        if(level == ERROR):
            str1 = "[ERROR] "
        if(level == FAILURE):
            str1 = "[FAILURE] "
        print(str1 + message)

# We define an object for representing a toothpick, which has two enpoints, as
# well as a centerpoint.
class Toothpick(object):
    def __init__(self, left, right, center):
        # Endpoints of a toothpick
        self.left        = left
        self.right       = right
        # Centerpoint of a toothpick
        self.center      = center

    def __repr__(self):
        out = str(self.left) + "&" + str(self.right)
        return out

# A representation of a board of toothpicks.
class Board(object):
    """
    This section of the class is in charge of managing the board toothpciks
    """
    # The toothpicks that have been placed on the board are represented as
    # elements in the board list.
    board = []
    # List of points that are occupied by one edge of a toothpick
    taken_once = []
    # List of points that have been occupied by two edges of toothpicks, and
    # therefore, no no other toothpick edge can be placed here.
    unavailable = []

    # The Board class can be initialized with an arbitrary list of toothpicks.
    def __init__(self, board):
        self.board = board

    # Returns True if a toothpick can be placed on the board. False otherwise
    def canBePlaced(self, toothpick):
        if ((toothpick.right in self.unavailable) or \
            (toothpick.left  in self.unavailable)):
            return False
        return True

    # Attempts to place a toothpick on the board. Returns True if the toothpick
    # was placed, and False when the toothpick could not be placed.
    def place(self, toothpick):
        if (self.canBePlaced(toothpick)):
            # add the toothpick to the board
            self.board.append(toothpick)
            log(DEBUG, 'toothpick was placed in the board')
            # add the edges to the corresponding taken_once, or unavailable lists
            if (toothpick.right in self.taken_once):
                self.unavailable.append(toothpick.right)
                log(DEBUG, 'Right edge of toothpick was added to unavailable list.')
            else:
                self.taken_once.append(toothpick.right)
                log(DEBUG, 'Right edge of toothpick was added to taken_once list.')
            if (toothpick.left in self.taken_once):
                self.unavailable.append(toothpick.left)
                log(DEBUG, 'Left edge of toothpick was added to unavailable list.')
            else:
                self.taken_once.append(toothpick.left)
                log(DEBUG, 'Left edge of toothpick was added to taken_once list.')

            # add the edges of the newly placed toothpick to the ready list for next iteration
            self.ready.append(toothpick.left)
            self.ready.append(toothpick.right)
            log(DEBUG, 'Added both edges of toothpick to the ready list')
            return True
        else:
            log(DEBUG, 'Toothpick cannot be placed')
            return False

    # Traverses the toothpicks on the board and modifies the taken_once and
    # unavailable lists accordingly.
    def audit_board(self):
        # TODO
        pass

    """
    This section of the class is realted to expanding the nodes.
    """
    ready = []
    expanded = []
    direction = LEFT
    # The board we will be working with
    board = None

    # expands all elements on the ready list
    def expand_ready(self):
        # The expanded list should always be empty at this point.
        if (not len(self.expanded) == 0):
            log(ERROR, 'Expanded list is not empty. Setting it to empty')
            self.expanded = []
        while (len(self.ready) != 0):
            # pop an edge from the ready list
            current_edge = self.ready.pop()
            # expand the current edge to obtain a toothpick
            expanded_toothpick = self.expand_edge(current_edge, n%2)
            # add the expanded toothpick to the expanded list
            self.expanded.append(expanded_toothpick)
            log(DEBUG, 'Added new toothpick to the expanded list')


    # expands an edge of a toothpick in a given direction to return a new toothpick
    def expand_edge(self, edge, direction):
        point1 = []
        point2 = []
        #construct toothpick
        if (direction == LEFT):
            point1 = [edge[X] + 1, edge[Y] - 1]
            point2 = [edge[X] - 1, edge[Y] + 1]
        if (direction == RIGHT):
            point1 = [edge[X] + 1, edge[Y] + 1]
            point2 = [edge[X] - 1, edge[Y] - 1]
        return Toothpick(point1, point2, edge)

    # Iterates over the toothpicks in the expanded list, deciding whether to place
    # the toothpick or not.
    def process_expanded_toothpicks(self):
        log(DEBUG, 'Processing toothpicks in the expanded list')
        while (len(self.expanded) != 0):
            # pop an edge from the expanded list
            current_toothpick = self.expanded.pop()
            # attempt to place the current toothpick on the board
            self.place(current_toothpick)

    # logs a brief summary of the class state
    def summary(self):
        log(INFO, 'Toothpicks on the board: ' + str(len(self.board)))
        log(INFO, str(self.board))
        log(INFO, 'Ready List (edges that will be expanded next:')
        log(INFO, str(self.ready))
        log(INFO, 'Expanded list (Toothpicks that will be (maybe) placed on the board:')
        log(INFO, str(self.expanded))



"""
 Program start
 Flow:
     1- Expand all edges in the ready list, this will put toothpicks in the expanded list.
     2- For every toothpick in the expanded list, decide if we should place the toothpick or not.
         2.1- The toothpcicks that we can be placed, will be appended to the place_next list.
     3- place all toothpicks in the next list.
"""
# Begin by placing a toothpick at center (0,0) and edges at (1,1) and (-1,-1).
# In this case, define a 45° orientation as True, and -45° orientation as False.
A = [1,1]
B = [-1,-1]
C = [0,0]
# create the initial toothpick
log(INFO, 'Creating initial toothpick')
initial_toothpick = Toothpick(A, B, C)
# create a new board
log(INFO, 'Creating new empty board')
board = Board([])

log(INFO, 'Adding the initial toothpick to the board')
board.place(initial_toothpick)
board.summary()

# Iterations consist on expanding the edges on the ready list, and then attempting
# to place all expanded toothpicks (processing) on the board.
while(n < MAX_ITERATIONS):
    log(INFO, '------------------------------------')
    log(INFO, 'beggining iteration number ' + str(n))
    log(INFO, 'Expanding edges on the ready list...')
    board.expand_ready()
    log(INFO, 'Done.')
    log(INFO, 'Processing expanded toothpicks...')
    board.process_expanded_toothpicks()
    log(INFO, 'Done.')
    log(INFO, 'End of iteration number ' + str(n))
    log(INFO, 'summary: ')
    board.summary()
    log(INFO, '====================================')

    # increase iteration number
    n += 1

log(INFO, 'End of calculation phase. Generatig points for plot.')


