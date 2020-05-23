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

# Initialize pygame
pygame.init()

# Create the game window
width = 1024
height = 656
screen = pygame.display.set_mode((width, height))
size = 40

# Title and Icon
pygame.display.set_caption("Path-Finding Algorithm")
pygame.display.set_icon(pygame.image.load('maze.png'))

# Two dimensional array of 0s - used for defining color of grid squares
array = [[0] * 25 for x in range(16)]  # 25 columns - 16 rows

num_columns = 25
num_rows = 16


# Background
def grid():
    for row in range(num_rows):
        for column in range(num_columns):
            color = white
            if array[row][column] == -1:
                color = green
            elif array[row][column] == -2:
                color = red
            elif array[row][column] == -3:
                color = black
            elif array[row][column] == 1:
                color = grey
            elif array[row][column] == 2:
                color = blue
            square = pygame.Rect(column * (size + 1), row * (1 + size), size, size)
            pygame.draw.rect(screen, color, square)


grid()

clock = pygame.time.Clock()


# Find Grid position from mouse click
def find_grid_position(posX, posY):
    def calc(base):
        x = math.floor(base / 40)
        return math.ceil((base - x) / 40)

    return calc(posX), calc(posY)


def find_start():
    start = ()
    for x in array:
        try:
            start = (array.index(x), x.index(-1))
        except ValueError:
            pass
    return start


def start_end():
    x = event.pos[0]
    y = event.pos[1]
    column, row = find_grid_position(x, y)
    if any(-2 in pos for pos in array):  # if any square is red, don't color any more squares
        pass
    elif any(-1 in pos for pos in array):
        if array[row - 1][column - 1] != -1:  # if not already green, turn red
            array[row - 1][column - 1] = -2
            grid()
            print('Grid position:', column, row)
            print('- End point selected')
    elif any(-1 in pos for pos in array) not in array:  # if no squares green, turn green
        array[row - 1][column - 1] = -1
        grid()
        print('Grid position:', column, row)
        print('- Start point selected')


# user-drawn obstacles
def obstacles():
    x = event.pos[0]
    y = event.pos[1]
    column, row = find_grid_position(x, y)
    if any(-2 in pos for pos in array) and any(-2 in pos for pos in array):
        # if not already green, red, or black, turn black
        if array[row - 1][column - 1] != -1 and array[row - 1][column - 1] != -2 and array[row - 1][column - 1] != -3:
            array[row - 1][column - 1] = -3
            grid()
            print('Grid position:', column, row)
            print('- Obstacle placed')


def depth_first_search(start_point):  # right -> up -> left -> down
    visited = [start_point]
    stack = [start_point]
    while len(stack) != 0:
        current = stack.pop()
        print('Current position:', current)

        if current not in visited:
            visited.append(current)
        grid()
        pygame.display.update()

        # stack takes last element - so we add in reverse priority
        # Down
        if array[current[0]][current[1]] != array[-1][current[1]]:
            if array[current[0] + 1][current[1]] == -2:
                break
            elif array[current[0] + 1][current[1]] == 0:
                stack.append((current[0] + 1, current[1]))
                print('Stack appended - Down - (', (current[0] + 1), current[1], ')')
        # Left
        if array[current[0]][current[1]] != array[current[0]][0]:
            if array[current[0]][current[1] - 1] == -2:
                break
            elif array[current[0]][current[1] - 1] == 0:
                stack.append((current[0], current[1] - 1))
                print('Stack appended - Left - (', current[0], (current[1] - 1), ')')
        # Up
        if array[current[0]][current[1]] != array[0][current[1]]:
            if array[current[0] - 1][current[1]] == -2:
                break
            elif array[current[0] - 1][current[1]] == 0:
                stack.append((current[0] - 1, current[1]))
                print('Stack appended - Up - (', (current[0] - 1), current[1], ')')
        # Right
        if array[current[0]][current[1]] != array[current[0]][-1]:
            if array[current[0]][current[1] + 1] == -2:
                break
            elif array[current[0]][current[1] + 1] == 0:
                stack.append(((current[0]), current[1] + 1))
                print('Stack appended - Right - (', current[0], (current[1] + 1), ')')

        # Recolor grid
        for x in stack:
            if array[x[0]][x[1]] != -1 and array[x[0]][x[1]] != -2:
                array[x[0]][x[1]] = 1  # 1 = grey
        for x in visited:
            if array[x[0]][x[1]] != -1 and array[x[0]][x[1]] != -2:  # -1 = green # -2 = red
                array[x[0]][x[1]] = 2  # 2 = blue

        time.sleep(.05)

    grid()
    pygame.display.update()


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X-Button is pressed --> quit program
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print('Enter key pressed')
                if find_start():
                    start = find_start()
                    print('- Start found', start)
                    depth_first_search(start)
                else:
                    print('- Start not found')
        elif event.type == pygame.MOUSEBUTTONDOWN:  # choose start and end point
            start_end()
        elif pygame.mouse.get_pressed()[0]:  # paint obstacles by holding mouse down
            obstacles()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
