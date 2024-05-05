import os
import pygame

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()

# Function to load images
def load_image(filename, level, transparent=True):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    formatted_filename = filename.format(level=level)
    image_path = os.path.join(script_directory, formatted_filename)
    
    if transparent:
        return pygame.image.load(image_path).convert_alpha()
    else:
        return pygame.image.load(image_path).convert()

# Load assets
def load_assets(level):
    ground_texture = load_image('grass{level}.png', level)
    ground_texture = pygame.transform.scale(ground_texture, (screen_width, screen_height - screen_height // 3 * 2))
    
    sky_texture = load_image('sky{level}.png', level)
    sky_texture = pygame.transform.scale(sky_texture, (screen_width, screen_height))
    
    enemy_texture = load_image('enemy{level}.png', level, transparent=True)
    enemy_texture = pygame.transform.scale(enemy_texture, (175, 175))
    
    player_texture = load_image('player{level}.png', level, transparent=True)
    player_texture = pygame.transform.scale(player_texture, (60, 60))
    
    enemy_ray_texture = load_image('enemy_fire{level}.png', level, transparent=True)
    enemy_ray_texture = pygame.transform.scale(enemy_ray_texture, (25, 25))
    
    return ground_texture, sky_texture, enemy_texture, player_texture, enemy_ray_texture