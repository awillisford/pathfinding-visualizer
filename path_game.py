import pygame
import math
import time

# Colors used
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)
yellow = (255, 255, 0)

# Attributes of graph
rows = 22
columns = 35
size = 30


def grid_position(posY, posX):
    def calc(pos):
        z = math.floor(pos / size)
        return math.ceil((pos - z) / size)

    return calc(posY), calc(posX)


def edge(array, side, node):
    if side == 'up':
        if array[node[0]][node[1]] == array[0][node[1]]:
            return True
    elif side == 'bottom':
        if array[node[0]][node[1]] == array[-1][node[1]]:
            return True
    elif side == 'left':
        if array[node[0]][node[1]] == array[node[0]][0]:
            return True
    elif side == 'right':
        if array[node[0]][node[1]] == array[node[0]][-1]:
            return True


def adjacent_square(array, direction, node):
    if direction == 'up':
        return array[node[0] - 1][node[1]]
    elif direction == 'bottom':
        return array[node[0] + 1][node[1]]
    elif direction == 'left':
        return array[node[0]][node[1] - 1]
    elif direction == 'right':
        return array[node[0]][node[1] + 1]


class Graph:
    def __init__(self):
        def resolution(x, y):
            return ((x + 1) * y) - 1

        self.screen = pygame.display.set_mode((resolution(size, columns), resolution(size, rows)))  # screen size
        self.matrix = [([0] * columns) for x in range(rows)]  # 2D array for changing grid colors

    # Create game window
    def draw_grid(self):
        for row in range(rows):
            for col in range(columns):
                color = white
                if self.matrix[row][col] == -1:
                    color = green
                elif self.matrix[row][col] == -2:
                    color = red
                elif self.matrix[row][col] == -3:
                    color = black
                elif self.matrix[row][col] == 1:
                    color = grey
                elif self.matrix[row][col] == 2:
                    color = blue
                elif self.matrix[row][col] == 3:
                    color = yellow
                square = pygame.Rect(col * (size + 1), row * (1 + size), size, size)
                pygame.draw.rect(self.screen, color, square)

    def create_start_end(self, event_pos_y, event_pos_x):
        row, column = grid_position(event_pos_y, event_pos_x)

        if any(-2 in square for square in self.matrix):  # if end point selected, pass
            pass

        elif any(-1 in square for square in self.matrix):  # if start point selected already
            if self.matrix[row - 1][column - 1] != -1:  # and selected square is not start point
                self.matrix[row - 1][column - 1] = -2  # create end point
                self.draw_grid()
                print('Grid position:', row, column)
                print('- End point selected')

        elif any(-1 in pos for pos in self.matrix) not in self.matrix:  # if no squares green, turn green
            self.matrix[row - 1][column - 1] = -1
            self.draw_grid()
            print('Grid position:', row, column)
            print('- Start point selected')

        pygame.display.update()

    def obstacles(self, event_pos_y, event_pos_x):
        row, column = grid_position(event_pos_y, event_pos_x)
        if self.matrix[row - 1][column - 1] == 0:
            self.matrix[row - 1][column - 1] = -3
            self.draw_grid()
            pygame.display.update()

    def find_start(self):
        start = ()
        for x in self.matrix:
            try:
                start = (self.matrix.index(x), x.index(-1))
            except ValueError:
                pass
        return start

    def get_unvisited_neighbors(self, square):
        unvisited_neighbors = []
        # Bottom
        if not edge(self.matrix, 'bottom', square):
            if self.matrix[square[0] + 1][square[1]] == 0 or self.matrix[square[0] + 1][square[1]] == -2:
                unvisited_neighbors.append((square[0] + 1, square[1]))
        # Left
        if not edge(self.matrix, 'left', square):
            if self.matrix[square[0]][square[1] - 1] == 0 or self.matrix[square[0]][square[1] - 1] == -2:
                unvisited_neighbors.append((square[0], square[1] - 1))
        # Up
        if not edge(self.matrix, 'up', square):
            if self.matrix[square[0] - 1][square[1]] == 0 or self.matrix[square[0] - 1][square[1]] == -2:
                unvisited_neighbors.append((square[0] - 1, square[1]))
        # Right
        if not edge(self.matrix, 'right', square):
            if self.matrix[square[0]][square[1] + 1] == 0 or self.matrix[square[0]][square[1] + 1] == -2:
                unvisited_neighbors.append((square[0], square[1] + 1))
        return unvisited_neighbors

    def backtrace(self, _dict_, start_child, start_point):
        child = start_child
        parent = 1
        while parent is not None:
            try:
                parent = _dict_[child]
                self.matrix[parent[0]][parent[1]] = 3
                child = parent
                time.sleep(.05)
            except KeyError:
                parent = None

            self.draw_grid()
            pygame.display.update()

        self.matrix[start_point[0]][start_point[1]] = -1
        self.draw_grid()
        pygame.display.update()

    def depth_first_search(self, start):  # right -> up -> left -> down
        visited = [start]
        stack = [start]
        child_parent = {}
        while len(stack) != 0:
            current = stack.pop()
            if current not in visited:
                visited.append(current)

            # update display
            self.draw_grid()
            pygame.display.update()

            # find unvisited squares and end point
            neighbor_squares = self.get_unvisited_neighbors(current)
            for square in neighbor_squares:
                child_parent[square] = current
                if self.matrix[square[0]][square[1]] == -2:
                    self.backtrace(child_parent, square, start)
                    return

                stack.append(square)

            # Recolor grid
            for x in stack:
                if self.matrix[x[0]][x[1]] != -1:
                    self.matrix[x[0]][x[1]] = 1  # 1 = grey
            for x in visited:
                if self.matrix[x[0]][x[1]] != -1:
                    self.matrix[x[0]][x[1]] = 2  # 2 = blue

            time.sleep(.05)
        self.draw_grid()
        pygame.display.update()


def main():
    # Initialize Game Window
    pygame.init()
    window = Graph()
    window.draw_grid()
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # exit button pressed -> quit program
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                y_pos = event.pos[1]
                window.create_start_end(y_pos, x_pos)
            elif pygame.mouse.get_pressed()[0]:
                x_pos = event.pos[0]
                y_pos = event.pos[1]
                if any(-2 in square for square in window.matrix):
                    window.obstacles(y_pos, x_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    window.depth_first_search(window.find_start())


main()
