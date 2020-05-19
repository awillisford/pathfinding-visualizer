import pygame
import math

# Colors used
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

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


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X-Button is pressed --> quit program
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # choose start and end point
            start_end()
        if pygame.mouse.get_pressed()[0]:  # paint obstacles by holding mouse down
            obstacles()

    pygame.display.update()
    clock.tick(30)

for x in array:
    print(x)
pygame.quit()
