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

    def depth_first_search(self, start):  # right -> up -> left -> down
        visited = [start]
        stack = [start]
        while len(stack) != 0:
            current = stack.pop()
            if current not in visited:
                visited.append(current)
            self.draw_grid()
            pygame.display.update()

            def edge(array, side):
                if side == 'up':
                    if array[current[0]][current[1]] == array[0][current[1]]:
                        return True
                elif side == 'bottom':
                    if array[current[0]][current[1]] == array[-1][current[1]]:
                        return True
                elif side == 'left':
                    if array[current[0]][current[1]] == array[current[0]][0]:
                        return True
                elif side == 'right':
                    if array[current[0]][current[1]] == array[current[0]][-1]:
                        return True

            def adjacent_square(array, direction):
                if direction == 'up':
                    return array[current[0] - 1][current[1]]
                elif direction == 'bottom':
                    return array[current[0] + 1][current[1]]
                elif direction == 'left':
                    return array[current[0]][current[1] - 1]
                elif direction == 'right':
                    return array[current[0]][current[1] + 1]

            # stack takes last element - so we add in reverse priority
            if not edge(self.matrix, 'bottom'):
                if adjacent_square(self.matrix, 'bottom') == -2:
                    break
                elif adjacent_square(self.matrix, 'bottom') == 0:
                    stack.append((current[0] + 1, current[1]))

            if not edge(self.matrix, 'left'):
                if adjacent_square(self.matrix, 'left') == -2:
                    break
                elif adjacent_square(self.matrix, 'left') == 0:
                    stack.append((current[0], current[1] - 1))

            if not edge(self.matrix, 'up'):
                if adjacent_square(self.matrix, 'up') == -2:
                    break
                elif adjacent_square(self.matrix, 'up') == 0:
                    stack.append((current[0] - 1, current[1]))

            if not edge(self.matrix, 'right'):
                if adjacent_square(self.matrix, 'right') == -2:
                    break
                elif adjacent_square(self.matrix, 'right') == 0:
                    stack.append((current[0], current[1] + 1))

            # Recolor grid
            for x in stack:
                if self.matrix[x[0]][x[1]] != -1:
                    self.matrix[x[0]][x[1]] = 1  # 1 = grey
            for x in visited:
                if self.matrix[x[0]][x[1]] != -1:
                    self.matrix[x[0]][x[1]] = 2  # 2 = blue

            time.sleep(.05)
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
