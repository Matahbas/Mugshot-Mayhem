import os
import random
import pygame
import pygame.font
from abc import ABC, abstractmethod
from pygame.locals import *
from assets import load_assets
from timer import Timer

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIME = (50, 205, 50)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Mugshot Mayhem")
ground_height = screen_height // 3 * 2

ground_texture, sky_texture, enemy_texture, player_texture, enemy_ray_texture = load_assets(3)

class CharacterFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def create_character(character_type, x, y, enemy_rays=None):
        if character_type == "player":
            return Player(x, y)
        elif character_type == "enemy":
            return Enemy(x, y, enemy_rays)
        
class Character(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, size, image, health):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.health = health
    
    @abstractmethod
    def calculate_health_bar_length(self):
        pass

    @abstractmethod
    def calculate_health_bar_color(self):
        pass

    def draw_health_bar(self, surface):
        bar_length = self.calculate_health_bar_length()
        bar_color = self.calculate_health_bar_color()

        filled_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_length, 10)
        pygame.draw.rect(surface, bar_color, filled_rect)

        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.size, 10)
        pygame.draw.rect(surface, BLACK, outline_rect, 2)

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 60, player_texture, 5)
        self.__speed_x = 5
        self.__speed_y = 0
        self.__gravity = 0.5
        self.jumping = False
        self.shooting = False
        self.__shoot_cooldown = 10
        self.__shoot_timer = 0

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.__speed_x
        if keys[pygame.K_d]:
            self.rect.x += self.__speed_x
        if keys[pygame.K_w] and not self.jumping:
            self.jump()
    
    def jump(self):
        self.jumping = True
        self.__speed_y -= 10
    
    def update_shooting(self):
        if self.health > 0 and self.__shoot_timer > 0:
            self.__shoot_timer -= 1

    def shoot(self, ray_group):
        if self.__shoot_timer <= 0:
            ray_group.add_ray(self.rect.x + self.size, self.rect.y + self.size // 2, 20)
            self.__shoot_timer = self.__shoot_cooldown

    def update(self, ground_height):
        self.__speed_y += self.__gravity
        if self.health > 0:
            self.rect.x = max(0, min(self.rect.x, screen_width - self.size))
        else:
            self.rect.x = max(0, min(self.rect.x, 1350 - self.size))
        self.rect.y = max(0, min(self.rect.y + self.__speed_y, ground_height - self.size))

        if self.rect.y + self.size >= ground_height:
            self.rect.y = ground_height - self.size
            self.__speed_y = 0
            self.jumping = False

    def calculate_health_bar_length(self):
        return self.size * (self.health / 5)
    
    def calculate_health_bar_color(self):
        red_component = min(max(255 - (self.health / 5) * 255, 0), 255)
        green_component = min(max((self.health / 5) * 255, 0), 255)
        return (red_component, green_component, 0)

    def handle_collision(self):
        self.health -= 1

class Enemy(Character):
    def __init__(self, x, y, enemy_rays):
        super().__init__(x, y, 175, enemy_texture, 100)
        self.__shoot_frequency = 60
        self.__shoot_timer = self.__shoot_frequency
        self.can_shoot = True
        self.enemy_rays = enemy_rays
        self.__teleport_frequency = 100
        self.__teleport_timer = self.__teleport_frequency
        self.__teleport_delay = 300
        self.__teleport_delay_timer = self.__teleport_delay
        self.teleporting = False

    def update(self):
        self.__shoot_timer -= 1
        if self.__shoot_timer <= 0:
            self.generate_rays()
            self.__shoot_timer = self.__shoot_frequency
        if not self.teleporting:
            self.__teleport_timer -= 1
            if self.__teleport_timer <= 0:
                self.teleport()
                self.teleporting = True
                self.__teleport_timer = self.__teleport_frequency

        elif self.teleporting:
            self.__teleport_delay_timer -= 1
            if self.__teleport_delay_timer <= 0:
                self.teleporting = False
                self.__teleport_delay_timer = self.__teleport_delay
                self.rect.x = -self.size
                self.rect.y = -self.size

    def generate_rays(self):
        if self.can_shoot:
            ray_y = random.randint(self.rect.y, self.rect.y + self.size - 15)
            ray = self.enemy_rays.add_ray(self.rect.x, ray_y, 5)
            ray.owner = self

    def teleport(self):
        self.rect.x = random.randint(0, screen_width - self.size)
        self.rect.y = ground_height - self.size

    def calculate_health_bar_length(self):
        return self.size * (self.health / 100)
    
    def calculate_health_bar_color(self):
        red_component = min(max(255 - self.health * 5, 0), 255)
        green_component = min(max(self.health * 5, 0), 255)
        return (red_component, green_component, 0)

class RayGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def add_ray(self, x, y, length):
        ray = Ray(x, y, length)
        self.add(ray)
        return ray

    def update(self, obstacles, enemy_alive, player_rect, enemy_rect):
        for ray in self.sprites():
            ray.move(player_rect, enemy_rect)
            if ray.rect.x <= 0 or ray.rect.x >= screen_width:
                self.remove(ray)
            elif not enemy_alive:
                self.remove(ray)
            else:
                hit_list = pygame.sprite.spritecollide(ray, obstacles, True)
                for target in hit_list:
                    self.remove(ray)
                    target.health -= 1
                    
    def draw(self, surface):
        for ray in self.sprites():
            if isinstance(ray.owner, Enemy):
                surface.blit(enemy_ray_texture, ray.rect)
            else:
                pygame.draw.rect(surface, LIME, ray.rect)

class Ray(pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        super().__init__()
        self.image = pygame.Surface((length, 2))
        self.image.fill(LIME)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.owner = None
    
    def move(self, player_rect, enemy_rect):
        if isinstance(self.owner, Enemy):
            target_y = player_rect.y + player_rect.height // 2
            if enemy_rect.x < player_rect.x:
                self.rect.x += 10
            else:
                self.rect.x -= 10
            if self.rect.y < target_y:
                self.rect.y += 1
            elif self.rect.y > target_y:
                self.rect.y -= 1
        else:
            if player_rect.x < enemy_rect.x:
                self.rect.x += 20
            else:
                self.rect.x -= 20

class Level3:
    def __init__(self, screen, screen_width, screen_height, timer):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.timer = timer
        self.setup()

    def display_message(self, text, font_size, color, position):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def setup(self):
        self.player_rays = RayGroup()
        self.enemy_rays = RayGroup()

        self.player = CharacterFactory.create_character("player", 20, ground_height - 60)
        self.enemy = CharacterFactory.create_character("enemy", 1350, ground_height - 175, self.enemy_rays)

        self.running = True

        self.player_won = False


    def update(self):
        elapsed_time = self.timer.get_elapsed_time()
        best_time = self.timer.read_best_time_from_file()
        self.screen.blit(sky_texture, (0, 0))
        self.screen.blit(ground_texture, (0, ground_height))

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r:
                    self.restart_game()

        keys = pygame.key.get_pressed() 

        self.player.move(keys)
        self.player.update_shooting()
        self.player.update(ground_height)

        if keys[K_SPACE] and self.player.health > 0:
            self.player.shoot(self.player_rays)

        self.enemy.update()
        if self.enemy.rect.colliderect(self.player.rect):
            self.player.health -= 1

        if self.player.health > 0:
            self.player.draw_health_bar(self.screen)
            self.screen.blit(player_texture, (self.player.rect.x, self.player.rect.y))
        else:
            self.enemy.can_shoot = False
            self.display_message("You lost", 100, (255, 0, 0), (self.screen_width // 2, self.screen_height // 2 - 10))
            self.display_message("Press 'r' to restart", 80, (255, 0, 0), (self.screen_width // 2, self.screen_height // 2 + 70))

        if self.enemy.health > 0:
            self.enemy.draw_health_bar(self.screen)
            self.screen.blit(enemy_texture, (self.enemy.rect.x, self.enemy.rect.y))
        else:
            self.enemy.can_shoot = False
            self.display_message("You won", 80, (0, 255, 0), (self.screen_width // 2, self.screen_height // 2))
            self.player_won = True

        self.player_rays.update(pygame.sprite.Group(self.enemy), self.enemy.health > 0, self.player.rect, self.enemy.rect)
        self.enemy_rays.update(pygame.sprite.Group(self.player), self.enemy.health > 0, self.player.rect, self.enemy.rect)
        
        self.player_rays.draw(self.screen)
        self.enemy_rays.draw(self.screen)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Time: {elapsed_time:.2f} seconds", True, (255, 255, 255))
        self.screen.blit(text_surface, (self.screen_width - text_surface.get_width() - 10, 10))
        if best_time != float('inf'):
            best_time_text_surface = font.render(f"Best Time: {best_time:.2f} seconds", True, (255, 255, 255))
        else:
            best_time_text_surface = font.render(f"Best Time: N/A", True, (255, 255, 255))
        self.screen.blit(best_time_text_surface, (self.screen_width - best_time_text_surface.get_width() - 10, 50))
        
        pygame.display.update()

        pygame.time.delay(15)

    def restart_game(self):
        self.player.health = 5
        self.enemy.health = 100

        self.player.rect.x = 20
        self.player.rect.y = ground_height - 60

        self.enemy.rect.x = 1350
        self.enemy.rect.y = ground_height - 175

        self.player_rays.empty()
        self.enemy_rays.empty()
        self.enemy.can_shoot = True