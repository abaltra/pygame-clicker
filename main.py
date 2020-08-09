# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import math
pygame.init()

class Circle:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.r = 2
        print(f"circle created at {self.pos[0]}, {self.pos[1]}")


S_WIDTH = 500
S_HEIGHT = 500
SCREEN_CROSS = math.sqrt(S_WIDTH**2 + S_HEIGHT**2)

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
running_circles = []

# Run until the user asks to quit
running = True
while running:

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos();
            running_circles.append(Circle(pos, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        if event.type == pygame.QUIT:
            running = False

    for i, circle in enumerate(running_circles):
        pygame.draw.circle(screen, circle.color, circle.pos, math.floor(circle.r), 2)
        circle.r += 0.1
        if (circle.r > SCREEN_CROSS):
            print(f"Removing cicle started in {circle.pos}")
            running_circles.pop(i)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()