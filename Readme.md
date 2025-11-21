Create a Pygame Window
1
2
3
Creating a window in Pygame is straightforward and involves initializing the library, setting up the display, and managing events to keep the window active. Below are the steps to achieve this.

1. Install Pygame Ensure Pygame is installed in your Python environment. Use the following command:

pip install pygame
Copier
2. Import and Initialize Pygame Start by importing the Pygame module and initializing it:

import pygame

# Initialize Pygame
pygame.init()
Copier
3. Create a Display Window Set up the display window using pygame.display.set_mode() and define its dimensions:

# Define window dimensions
width, height = 800, 600

# Create the window
screen = pygame.display.set_mode((width, height))

# Set a title for the window
pygame.display.set_caption("Pygame Window Example")
Copier
4. Add Background Color and Keep Window Active Fill the screen with a background color and use an event loop to keep the window open:

# Define background color (RGB)
background_color = (0, 128, 255) # Blue

# Fill the screen with the background color
screen.fill(background_color)

# Update the display
pygame.display.flip()

# Event loop to keep the window running
running = True
while running:
for event in pygame.event.get():
if event.type == pygame.QUIT: # Check for quit event
running = False

# Quit Pygame
pygame.quit()
Copier
5. Run the Program Save this code in a .py file and run it. A window with a blue background will appear, which can be closed by clicking the close button.