import pygame
import sys
from level1 import Level1
from level2 import Level2
from level3 import Level3
from timer import Timer

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mugshot Mayhem")

timer = Timer()
timer.start()

levels = [Level1(screen, screen_width, screen_height, timer),
          Level2(screen, screen_width, screen_height, timer),
          Level3(screen, screen_width, screen_height, timer)]

current_level = 0
running = True

while running and current_level < len(levels):
    level = levels[current_level]

    while level.running:
        level.update()  

        if level.running == False:
            running = False

        elif level.player_won:
            if current_level == len(levels) - 1:
                elapsed_time = timer.get_elapsed_time()
                timer.write_elapsed_time_to_file(elapsed_time)
                timer.stop()
            else:
                level.running = False
                current_level += 1

pygame.quit()

sys.exit()