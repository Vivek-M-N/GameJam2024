import arcade
import pygame
import numpy as np
import math
import os
import tkinter as tk
from tkinter import messagebox

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"
GRAVITY = 9.8 * 10  # Gravity constant


class MainMenu(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Press P to Play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press E to Experiment", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.E:
            root = tk.Tk()
            app = ConfigApp(root)
            root.mainloop()
            self.window.show_view(self)

class GameView(arcade.View):

    #INIT
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Background.jpg")
        self.bg_scale = self.background.width / SCREEN_WIDTH
        self.level = 1
        self.ball = Circle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.mouse_pressed = False
        self.mouse_released = False
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0

        # Load the hoop texture
        self.hoop_texture = arcade.load_texture("hoop.png")

        if self.level == 1:
            self.walls = [
                (SCREEN_WIDTH - 120, SCREEN_HEIGHT / 2, 10, 100),
                (SCREEN_WIDTH - 70, SCREEN_HEIGHT / 2 - 50, 100, 10),
                (SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2, 10, 100)]
            self.target_zone = ((1000+self.ball.RADIUS,260+self.ball.RADIUS),(1100-self.ball.RADIUS,460-self.ball.RADIUS*3))
        elif self.level == 2:
            self.walls = [
                (SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2, 10, 200),
                (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2 - 100, 200, 10),
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT / 2, 10, 200)]
            self.target_zone = ((1000+self.ball.RADIUS,260+self.ball.RADIUS),(1100-self.ball.RADIUS,460-self.ball.RADIUS*2.5))
        
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
                self.level_up()

        for surface in self.slanted_surfaces:
            if self.check_slanted_surface_collision(surface):
                self.reflect_from_slanted_surface(surface)

        if self.check_curved_surface_collision():
            self.reflect_from_curved_surface()

        for line in self.hoop_lines:
            if self.check_slanted_surface_collision(line):
                self.reflect_from_slanted_surface(line)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.ball.reset()

    def ball_in_target_zone(self):
        return self.target_zone[0][0] < self.ball.x < self.target_zone[1][0] and self.target_zone[0][1] < self.ball.y < self.target_zone[1][1]

    def level_up(self):
        if self.level < 2:
            self.level += 1
            self.ball = Circle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        else:
            messagebox.showinfo("Congratulations", "You have completed all levels!")
            arcade.close_window()

    def check_slanted_surface_collision(self, surface):
        surface_start, surface_end = surface
        ball_to_surface_start = np.array([self.ball.x - surface_start[0], self.ball.y - surface_start[1]])
        surface_vector = np.array([surface_end[0] - surface_start[0], surface_end[1] - surface_start[1]])
        surface_length = np.linalg.norm(surface_vector)
        surface_unit_vector = surface_vector / surface_length
        projection_length = np.dot(ball_to_surface_start, surface_unit_vector)
        if 0 <= projection_length <= surface_length:
            closest_point = surface_start + projection_length * surface_unit_vector
            distance_to_surface = np.linalg.norm(np.array([self.ball.x, self.ball.y]) - closest_point)
            return distance_to_surface < self.ball.RADIUS
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

class Circle:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.color = (255, 255, 255)
        self.RADIUS = 30
        self.name = str(Circle.count)
        self.mass = 300
        self.cd = 0.47
        self.area = 1
        self.rho = 1.15
        self.timestep = 1
        self.g = 9.81 * 50
        self.vx = 0
        self.vx_new = 0
        self.vy = 0
        self.vy_new = 0
        self.ax = 0
        self.ay = 0
        Circle.count += 1
        self.e = 0.9

        self.texture = arcade.load_texture("ball.png")

        self.load_config()

    def load_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as file:
                config = eval(file.read())
                self.mass = config.get("Mass (kg)", self.mass)
                self.cd = config.get("Drag Coefficient (-)", self.cd)
                self.area = config.get("Area (m^2)", self.area)
                self.rho = config.get("Air Density (kg/m^3)", self.rho)
                self.g = config.get("Acceleration due to gravity (m/s^2)", self.g)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.RADIUS, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.RADIUS * 2, self.RADIUS * 2, self.texture)

    def update(self, delta_time):
        alpha = (self.rho * self.area * self.cd * delta_time) / (2 * self.mass) * np.sign(self.vx)
        if self.vx == 0:
            self.vx_new = 0
        else:
            self.vx_new = [(1 + math.sqrt(1+4*alpha*(self.vx)))/(-2*alpha)]
            self.vx_new.append((1 - math.sqrt(1+4*alpha*(self.vx)))/(-2*alpha))
            self.vx_new = np.asarray(self.vx_new)
            self.vx_new = self.vx_new.flat[np.abs(self.vx_new - self.vx).argmin()]
        self.ax = (self.vx_new - self.vx) / delta_time
        self.x += self.vx_new * delta_time
        
        if self.x < 0+self.RADIUS :
            self.x = 0+self.RADIUS+1
            self.vx = -self.e*self.vx_new 
        elif self.x > SCREEN_WIDTH-self.RADIUS-1:
            self.x = SCREEN_WIDTH-self.RADIUS
            self.vx = -self.e*self.vx_new
        else:
            self.vx = self.vx_new
          
        alpha = (self.rho * self.area * self.cd * delta_time) / (2 * self.mass) * np.sign(self.vy)
        if self.vy == 0:
            self.vy_new = 0
        else:
            self.vy_new = [(1 + math.sqrt(1+4*alpha*(self.vy-self.g*delta_time)))/(-2*alpha)]
            self.vy_new.append((1 - math.sqrt(1+4*alpha*(self.vy-self.g*delta_time)))/(-2*alpha))
            self.vy_new = np.asarray(self.vy_new)
            self.vy_new = self.vy_new.flat[np.abs(self.vy_new - self.vy).argmin()]
        self.ay = (self.vy_new - self.vy) / delta_time
        self.y += self.vy_new * delta_time
        
        if self.y < 0+self.RADIUS:
            self.y = 0+self.RADIUS+1
            self.vy = -self.e*self.vy_new
        elif self.y > SCREEN_HEIGHT-self.RADIUS:
            self.y = SCREEN_HEIGHT-self.RADIUS-1
            self.vy = -self.e*self.vy_new
        else:
            self.vy = self.vy_new

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.vx = 0
        self.vy = 0



class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Configuration")
        self.display_parameters = {
            "Mass (kg)": 300,
            "Drag Coefficient (-)": 0.47,
            "Area (m^2)": 1,
            "Air Density (kg/m^3)": 1.15,
            "Acceleration due to gravity (m/s^2)": 9.81
        }
        self.actual_parameters = {
            "Mass (kg)": 300,
            "Drag Coefficient (-)": 0.47,
            "Area (m^2)": 1,
            "Air Density (kg/m^3)": 1.15,
            "Acceleration due to gravity (m/s^2)": 9.81*50
        }
        self.resolutions = {
            "Mass (kg)": 1,
            "Drag Coefficient (-)": 0.1,
            "Area (m^2)": 0.1,
            "Air Density (kg/m^3)": 0.01,
            "Acceleration due to gravity (m/s^2)": 0.01
        }
        self.limits = {
            "Mass (kg)": (0.1, 3000),
            "Drag Coefficient (-)": (0.01, 10),
            "Area (m^2)": (0.1, 10),
            "Air Density (kg/m^3)": (0.1, 10),
            "Acceleration due to gravity (m/s^2)": (0.1, 10*9.81)
        }
        self.sliders = {}
        self.create_sliders()

    def create_sliders(self):
        row = 0
        for key, value in self.display_parameters.items():
            label = tk.Label(self.root, text=key)
            label.grid(row=row, column=0, padx=10, pady=10)
            resolution = self.resolutions.get(key, 0.01)
            lower_limit, upper_limit = self.limits.get(key, (0, value * 2))
            slider = tk.Scale(self.root, from_=lower_limit, to=upper_limit, orient=tk.HORIZONTAL, resolution=resolution)
            slider.set(value)
            slider.grid(row=row, column=1, padx=10, pady=10)
            self.sliders[key] = slider
            row += 1

        save_button = tk.Button(self.root, text="Save", command=self.save_config)
        save_button.grid(row=row, columnspan=2, padx=10, pady=10)

    def save_config(self):
        for key, slider in self.sliders.items():
            if key == "Acceleration due to gravity (m/s^2)":
                self.actual_parameters[key] = float(slider.get()) * 50
            else:
                self.actual_parameters[key] = float(slider.get())
        
        with open("config.txt", "w") as file:
            file.write(str(self.actual_parameters))
        
        messagebox.showinfo("Configuration Saved", "Configuration has been saved successfully!")
        self.root.destroy()

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("The Entertainer.mp3")
    pygame.mixer.music.play(-1)  # Play music indefinitely (-1)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()
