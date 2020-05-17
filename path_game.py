import pygame
import math

# Colors used
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

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

# Two dimensional array of 0s
array = [[0] * 25 for x in range(16)]  # 25 columns - 16 rows

num_columns = 25
num_rows = 16


# Background
def grid():
    for row in range(num_rows):
        for column in range(num_columns):
            color = white
            if array[row][column] == 1:
                color = green
            elif array[row][column] == 2:
                color = red
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


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        # X-Button is pressed --> quit program
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos
            column, row = find_grid_position(x, y)
            print('Grid position:', column, row)
            if any(2 in x for x in array):                # if any square is red, don't color any more squares
                pass
            elif any(1 in x for x in array):
                if array[row - 1][column - 1] != 1:       # if not already green, turn red
                    array[row - 1][column - 1] = 2
                    grid()
                    print('- End point selected')
            elif any(1 in x for x in array)not in array:  # if no squares green, turn green
                array[row - 1][column - 1] = 1
                grid()
                print('- Start point selected')

    pygame.display.update()
    clock.tick(30)

print(array)
pygame.quit()
