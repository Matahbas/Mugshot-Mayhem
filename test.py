import unittest
from unittest.mock import patch, MagicMock
import pygame
from level1 import Player, Enemy, RayGroup, Ray

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(50, 100)

    @patch('pygame.key.get_pressed')
    def test_player_movement(self, mock_get_pressed):
        mock_get_pressed.return_value = {
            pygame.K_w: False,
            pygame.K_a: True,
            pygame.K_d: False
        }
        self.player.move(mock_get_pressed.return_value)
        self.assertEqual(self.player.rect.x, 50 - self.player.speed_x)

        mock_get_pressed.return_value = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_d: True
        }
        self.player.move(mock_get_pressed.return_value)
        self.assertEqual(self.player.rect.x, 50)

    @patch('pygame.key.get_pressed')
    @patch.object(Player, 'shoot')
    def test_player_shoot(self, mock_shoot, mock_get_pressed):
        mock_get_pressed.return_value = {}
        self.player.shoot({})
        mock_shoot.assert_called_once()

    def test_shoot_timer_initial_value(self):
        self.assertEqual(self.player.shoot_timer, 0)

    def test_player_health_decrease(self):
        initial_health = self.player.health
        self.player.health -= 1
        self.assertEqual(self.player.health, initial_health - 1)

    @patch('pygame.sprite.spritecollide')
    def test_collision_detection(self, mock_spritecollide):
        mock_spritecollide.return_value = [MagicMock()]
        initial_health = self.player.health
        self.player.handle_collision()
        self.assertEqual(self.player.health, initial_health - 1)

class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy_rays = RayGroup()
        self.enemy = Enemy(200, 100, self.enemy_rays)

    def test_enemy_health_decrease(self):
        initial_health = self.enemy.health
        self.enemy.health -= 10
        self.assertEqual(self.enemy.health, initial_health - 10)

    def test_enemy_ray_generation(self):
        self.enemy.generate_rays()
        self.assertTrue(isinstance(self.enemy_rays.sprites()[0], Ray))

class TestRayGroup(unittest.TestCase):
    def setUp(self):
        self.ray_group = RayGroup()

    def test_add_ray(self):
        ray = self.ray_group.add_ray(50, 100, 20)
        self.assertTrue(isinstance(ray, Ray))
        self.assertIn(ray, self.ray_group.sprites())

if __name__ == '__main__':
    unittest.main()