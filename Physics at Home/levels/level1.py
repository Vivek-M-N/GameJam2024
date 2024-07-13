import arcade
import tkinter as tk
import numpy as np
import math
from tkinter import messagebox
from circle import Circle
from config_app import ConfigApp

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Level1(arcade.View):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.background = arcade.load_texture("assets/Background.jpg")
        self.bg_scale = self.background.width / SCREEN_WIDTH
        self.level = 1
        self.windx = 0
        self.windy = 0
        self.mouse_pressed = False
        self.mouse_released = False
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0

        self.ball = Circle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.windx, self.windy)

        self.target_zone = ((1000 + self.ball.RADIUS, 260 + self.ball.RADIUS), (1200 - self.ball.RADIUS, 460 - self.ball.RADIUS * 2.5))

        # Load the hoop texture
        self.hoop_texture = arcade.load_texture("assets/hoop.png")

        self.slanted_surfaces = [
            ((200, 200), (400, 400)),  # Example coordinates
            ((500, 100), (700, 300)),
            ((300, 400), (600, 500)),
            ((100, 600), (300, 700)),
        ]

        self.curved_surface = {
            'center': (800, 400),
            'radius': 100,
            'start_angle': 0,
            'end_angle': 180
        }

        # Lines around the hoop
        self.hoop_lines = [
            ((1000, 260), (1000, 360)),  # Left line
            ((1000, 260), (1100, 260)),  # Bottom line
            ((1100, 260), (1100, 460)),  # Right line
        ]

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.ball.draw()
        if self.mouse_pressed:
            arcade.draw_line(self.ball.x, self.ball.y, self.current_x, self.current_y, arcade.color.BLACK)

        arcade.draw_text(f"Level {self.level}", SCREEN_WIDTH * 0.025, SCREEN_HEIGHT - 69, arcade.color.BLACK, 20)

        # Draw the hoop images instead of walls
        arcade.draw_texture_rectangle(1050, 360, 100, 200, self.hoop_texture)

        for surface in self.slanted_surfaces:
            arcade.draw_line(surface[0][0], surface[0][1], surface[1][0], surface[1][1], arcade.color.RED, 5)

        arcade.draw_arc_outline(
            self.curved_surface['center'][0],
            self.curved_surface['center'][1],
            self.curved_surface['radius'] * 2,
            self.curved_surface['radius'] * 2,
            arcade.color.RED,
            self.curved_surface['start_angle'],
            self.curved_surface['end_angle'],
            5
        )

        # Draw hoop lines
        for line in self.hoop_lines:
            arcade.draw_line(line[0][0], line[0][1], line[1][0], line[1][1], arcade.color.BLACK, 3)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pressed = True
        self.start_x = x
        self.start_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = False
        self.mouse_released = True
        self.ball.vx = (self.start_x - x) * 5
        self.ball.vy = (self.start_y - y) * 5

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self.current_x = x
            self.current_y = y

    def on_update(self, delta_time):
        if self.mouse_released:
            self.ball.update(delta_time)
            if self.ball_in_target_zone():
                from levels.level2 import Level2
                game_view = Level2()
                self.window.show_view(game_view)

        for surface in self.slanted_surfaces:
            if self.check_slanted_surface_collision(surface):
                self.reflect_from_slanted_surface(surface)
            if self.check_slanted_surface_corner(surface):
                self.ball.vx *= -self.ball.e
                self.ball.vy *= -self.ball.e
                self.ball.x += self.ball.vx*0.01
                self.ball.y += self.ball.vy*0.01

        if self.check_curved_surface_collision():
            self.reflect_from_curved_surface()

        for line in self.hoop_lines:
            if self.check_slanted_surface_collision(line):
                self.reflect_from_slanted_surface(line)
            if self.check_slanted_surface_corner(line):
                self.ball.vx *= -self.ball.e
                self.ball.vy *= -self.ball.e
                self.ball.x += self.ball.vx*0.01
                self.ball.y += self.ball.vy*0.01

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.ball.reset()
        elif key == arcade.key.E:
            root = tk.Tk()
            app = ConfigApp(root)
            root.mainloop()
            self.window.show_view(self)
            self.ball.load_config()
            # self.ball.reset()

    def ball_in_target_zone(self):
        return self.target_zone[0][0] < self.ball.x < self.target_zone[1][0] and self.target_zone[0][1] < self.ball.y < self.target_zone[1][1]

    def check_slanted_surface_collision(self, surface):
        surface_start, surface_end = surface
        ball_to_surface_start = np.array([self.ball.x - surface_start[0], self.ball.y - surface_start[1]])
        ball_to_surface_end = np.array([self.ball.x - surface_end[0], self.ball.y - surface_end[1]])
        surface_vector = np.array([surface_end[0] - surface_start[0], surface_end[1] - surface_start[1]])
        surface_length = np.linalg.norm(surface_vector)
        surface_unit_vector = surface_vector / surface_length
        projection_length = np.dot(ball_to_surface_start, surface_unit_vector)
        if 0 <= projection_length <= surface_length:
            closest_point = surface_start + projection_length * surface_unit_vector
            distance_to_surface = np.linalg.norm(np.array([self.ball.x, self.ball.y]) - closest_point)
            return distance_to_surface < self.ball.RADIUS
        return False
    
    def check_slanted_surface_corner(self,surface):
        surface_start, surface_end = surface
        ball_to_surface_start = np.array([self.ball.x - surface_start[0], self.ball.y - surface_start[1]])
        ball_to_surface_end = np.array([self.ball.x - surface_end[0], self.ball.y - surface_end[1]])
        #print(math.sqrt(ball_to_surface_start[0]**2+ball_to_surface_start[1]**2))
        if math.sqrt(ball_to_surface_start[0]**2+ball_to_surface_start[1]**2) < self.ball.RADIUS+5 or math.sqrt(ball_to_surface_end[0]**2+ball_to_surface_end[1]**2) < self.ball.RADIUS+5:
            return True
        return False

    def reflect_from_slanted_surface(self, surface):
        surface_start, surface_end = surface
        surface_vector = np.array([surface_end[0] - surface_start[0], surface_end[1] - surface_start[1]])
        surface_normal = np.array([-surface_vector[1], surface_vector[0]], dtype=float)
        surface_normal /= np.linalg.norm(surface_normal)
        velocity_vector = np.array([self.ball.vx, self.ball.vy])
        reflected_velocity = velocity_vector - 2 * np.dot(velocity_vector, surface_normal) * surface_normal
        self.ball.vx, self.ball.vy = reflected_velocity * self.ball.e
        self.ball.x += self.ball.vx * 0.01
        self.ball.y += self.ball.vy * 0.01

    def check_curved_surface_collision(self):
        center = self.curved_surface['center']
        radius = self.curved_surface['radius']
        ball_to_center = np.array([self.ball.x - center[0], self.ball.y - center[1]])
        distance_to_center = np.linalg.norm(ball_to_center)
        if abs(distance_to_center - radius) < self.ball.RADIUS:
            angle = math.degrees(math.atan2(ball_to_center[1], ball_to_center[0]))
            if self.curved_surface['start_angle'] <= angle <= self.curved_surface['end_angle']:
                return True
        return False

    def reflect_from_curved_surface(self):
        center = self.curved_surface['center']
        ball_to_center = np.array([self.ball.x - center[0], self.ball.y - center[1]])
        surface_normal = ball_to_center / np.linalg.norm(ball_to_center)
        velocity_vector = np.array([self.ball.vx, self.ball.vy])
        reflected_velocity = velocity_vector - 2 * np.dot(velocity_vector, surface_normal) * surface_normal
        self.ball.vx, self.ball.vy = reflected_velocity * self.ball.e
        self.ball.x += self.ball.vx * 0.01
        self.ball.y += self.ball.vy * 0.01
