import pygame
import math
import time
from GUI import gui_settings

# Colors used
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
grey = (169, 169, 169)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Color codes used
cc_black = -3
cc_red = -2
cc_green = -1
cc_white = 0
cc_grey = 1
cc_blue = 2
cc_yellow = 3

# Attributes of graph
attribute_list = gui_settings()  # from GUI file
rows = attribute_list[1]
columns = attribute_list[2]
size = attribute_list[3]


def grid_position(posY, posX):
    def calc(pos):
        z = math.floor(pos / size)
        return math.floor((pos - z) / size)

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


def adjacent_color(array, direction, node):
    if direction == 'up':
        return array[node[0] - 1][node[1]]
    elif direction == 'bottom':
        return array[node[0] + 1][node[1]]
    elif direction == 'left':
        return array[node[0]][node[1] - 1]
    elif direction == 'right':
        return array[node[0]][node[1] + 1]


class Window:
    def __init__(self):
        def resolution(size_square, columns_rows):
            return ((size_square + 1) * columns_rows) - 1

        self.screen = pygame.display.set_mode((resolution(size, columns), resolution(size, rows)))  # screen size
        self.matrix = [([0] * columns) for x in range(rows)]  # 2D array for changing grid colors

    # Create grid inside game window
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
        pygame.display.update()

    def create_start_end(self, event_pos_y, event_pos_x):
        row, column = grid_position(event_pos_y, event_pos_x)
        if any(cc_red in square for square in self.matrix):  # if end point selected, pass
            pass
        elif any(cc_green in square for square in self.matrix):  # if start point selected already
            if self.matrix[row][column] != cc_green:  # and selected square is not start point
                self.matrix[row][column] = cc_red  # - create end point
                self.draw_grid()
                print('Grid position:', row, column)
                print('- End point selected')
        elif any(cc_green in pos for pos in self.matrix) not in self.matrix:  # if no squares green, turn green
            self.matrix[row][column] = cc_green
            self.draw_grid()
            print('Grid position:', row, column)
            print('- Start point selected')

    def obstacles(self, event_pos_y, event_pos_x):
        row, column = grid_position(event_pos_y, event_pos_x)
        if self.matrix[row][column] == cc_white:
            self.matrix[row][column] = cc_black
            self.draw_grid()

    def find_start(self):
        start = ()
        for x in self.matrix:
            try:
                start = (self.matrix.index(x), x.index(-1))
            except ValueError:
                pass
        return start

    def get_unvisited_neighbors(self, square):
        neighbors = []
        # Bottom
        if not edge(self.matrix, 'bottom', square):
            if self.matrix[square[0] + 1][square[1]] == cc_white or self.matrix[square[0] + 1][square[1]] == cc_red:
                neighbors.append((square[0] + 1, square[1]))
        # Left
        if not edge(self.matrix, 'left', square):
            if self.matrix[square[0]][square[1] - 1] == cc_white or self.matrix[square[0]][square[1] - 1] == cc_red:
                neighbors.append((square[0], square[1] - 1))
        # Up
        if not edge(self.matrix, 'up', square):
            if self.matrix[square[0] - 1][square[1]] == cc_white or self.matrix[square[0] - 1][square[1]] == cc_red:
                neighbors.append((square[0] - 1, square[1]))
        # Right
        if not edge(self.matrix, 'right', square):
            if self.matrix[square[0]][square[1] + 1] == cc_white or self.matrix[square[0]][square[1] + 1] == cc_red:
                neighbors.append((square[0], square[1] + 1))
        return neighbors

    def backtrace(self, _dict_, start_child, start_point):
        child = start_child
        while True:
            try:
                parent = _dict_[child]
                self.matrix[parent[0]][parent[1]] = cc_yellow
                child = parent
                time.sleep(.01)
            # if next to start
            except KeyError:
                break

            self.draw_grid()

        self.matrix[start_point[0]][start_point[1]] = cc_green
        self.draw_grid()

    def depth_first_search(self, start):  # right -> up -> left -> down
        visited = []
        stack = [start]
        child_parent = {}
        while len(stack) != 0:
            current = stack.pop()

            if current in visited:
                continue
            else:
                visited.append(current)

            # update display
            self.draw_grid()

            # find unvisited squares and end point
            neighbor_squares = self.get_unvisited_neighbors(current)
            for square in neighbor_squares:
                child_parent[square] = current
                if self.matrix[square[0]][square[1]] == cc_red:
                    self.backtrace(child_parent, square, start)
                    return
                stack.append(square)

            # Recolor grid
            for x in stack:
                if self.matrix[x[0]][x[1]] != cc_green:  # if not start
                    self.matrix[x[0]][x[1]] = cc_grey  # turn stack grey
            for x in visited:
                if self.matrix[x[0]][x[1]] != cc_green:  # if not start
                    self.matrix[x[0]][x[1]] = cc_blue  # turn visited blue

            time.sleep(.02)
        self.draw_grid()

    def breadth_first_search(self, start):
        visited = []
        queue = [start]
        child_parent = {}
        while len(queue) != 0:
            current = queue.pop()

            if current in visited:
                continue
            else:
                visited.append(current)

            # update display
            self.draw_grid()

            # find unvisited squares and end point
            neighbor_squares = self.get_unvisited_neighbors(current)
            for square in neighbor_squares:
                child_parent[square] = current
                if self.matrix[square[0]][square[1]] == cc_red:
                    self.backtrace(child_parent, square, start)
                    return
                queue.insert(0, square)

            # Recolor grid
            for x in queue:
                if self.matrix[x[0]][x[1]] != cc_green:  # if not start
                    self.matrix[x[0]][x[1]] = cc_grey  # turn stack grey
            for x in visited:
                if self.matrix[x[0]][x[1]] != cc_green:  # if not start
                    self.matrix[x[0]][x[1]] = cc_blue  # turn visited blue

            time.sleep(.01)
        self.draw_grid()


def main():
    # Initialize Game Window
    pygame.init()
    game = Window()
    game.draw_grid()

    # Game Loop
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:  # exit button pressed -> quit program
            break
        elif pygame.mouse.get_pressed()[0]:
            x_pos = event.pos[0]
            y_pos = event.pos[1]
            game.create_start_end(y_pos, x_pos)
            if any(cc_red in square for square in game.matrix):
                game.obstacles(y_pos, x_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if attribute_list[0] == 'Depth first search':
                    game.depth_first_search(game.find_start())
                elif attribute_list[0] == 'Breadth first search':
                    game.breadth_first_search(game.find_start())


main()
