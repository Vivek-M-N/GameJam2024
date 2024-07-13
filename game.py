import arcade
import numpy as np
import math
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"
GRAVITY = 9.8 * 10  # Gravity constant

BASKET = [
    ((1000, 460), (1000, 260)),
    ((1000, 260), (1100, 260)),
    ((1100, 260), (1100, 460))
]   

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
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Background.jpg")
        self.bg_scale = self.background.width / SCREEN_WIDTH
        self.level = 1
        self.load_level()
        self.ball = Circle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.mouse_pressed = False
        self.mouse_released = False
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0

    def load_level(self):
        if self.level == 1:
            self.walls = [
                (SCREEN_WIDTH - 60, SCREEN_HEIGHT / 3, 10, 100),
                (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 3 - 50, 100, 10),
                (SCREEN_WIDTH - 20, SCREEN_HEIGHT / 3, 10, 100)]
        elif self.level == 2:
            self.walls = [
                (SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2, 10, 200),
                (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2 - 100, 200, 10),
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT / 2, 10, 200)]
        # Add more levels as needed

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.ball.draw()
        if self.mouse_pressed:
            arcade.draw_line(self.ball.x, self.ball.y, self.current_x, self.current_y, arcade.color.BLACK)
            self.draw_trajectory(self.ball.x, self.ball.y, self.current_x, self.current_y)

        for wall in self.walls:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.ALLOY_ORANGE)

        for wall in BASKET:
            arcade.draw_line(wall[0][0], wall[0][1], wall[1][0], wall[1][1], arcade.color.BLACK, 2)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pressed = True
        self.start_x = x
        self.start_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = False
        self.mouse_released = True
        # Calculate the initial velocities based on the drag distance
        self.ball.vx = (self.start_x - x) * 5  # Adjust scaling factor as needed
        self.ball.vy = (self.start_y - y) * 5  # Adjust scaling factor as needed

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self.current_x = x
            self.current_y = y

    def draw_trajectory(self, start_x, start_y, current_x, current_y):
        velocity_x = (start_x - current_x)  # Adjust scaling factor as needed
        velocity_y = (start_y - current_y)  # Adjust scaling factor as needed

        for t in range(1, 100):  # Increase range for a longer trajectory
            t /= 10  # Scale time down
            end_x = start_x + velocity_x * t
            end_y = start_y + velocity_y * t - 0.5 * GRAVITY * t ** 2

            if end_y < self.ball.RADIUS or end_y > SCREEN_HEIGHT - self.ball.RADIUS or end_x < self.ball.RADIUS or end_x > SCREEN_WIDTH - self.ball.RADIUS:  # Stop if it hits the ground
                break

            arcade.draw_circle_filled(end_x, end_y, 2, arcade.color.ORANGE)

    
    def on_update(self, delta_time):
        if self.mouse_released:
            self.ball.update(delta_time)
        if self.ball.x  < SCREEN_WIDTH - 100 and self.ball.x > SCREEN_WIDTH - 300 and self.ball.y < SCREEN_HEIGHT - 100 and self.ball.y > SCREEN_HEIGHT - 300: #change to whatever 
                self.level += 1
                print(self.level)
                if self.level > 2:  # Replace with the total number of levels
                    self.level = 1  # Restart at the first level
                self.load_level()
                self.ball.x=SCREEN_WIDTH / 2
                self.ball.y=SCREEN_HEIGHT / 2
                self.mouse_released = False            
            
    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.R:
            self.ball.reset()

class Circle:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.color = (255, 0, 0)
        self.RADIUS = 30
        self.name = str(Circle.count)
        self.mass = 300  # Default value
        self.cd = 0.47  # Default value
        self.area = 1  # Default value
        self.rho = 1.15  # Default value
        self.timestep = 1
        self.g = 9.81 * 50  # Default value
        self.vx = 0
        self.vx_new = 0
        self.vy = 0
        self.vy_new = 0
        self.ax = 0
        self.ay = 0
        Circle.count += 1
        self.e = 0.9

        self.load_config()

    def load_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as file:
                config = eval(file.read())
                self.mass = config.get("Mass", self.mass)
                self.cd = config.get("Drag Coefficient", self.cd)
                self.area = config.get("Area", self.area)
                self.rho = config.get("Air Density", self.rho)
                self.g = config.get("Gravity", self.g)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.RADIUS, self.color)
        arcade.draw_text(self.name, self.x - 7, self.y - 7, arcade.color.WHITE, font_size=15)

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
        self.x += self.vx_new * delta_time * 2
        
        if self.x < 0+self.RADIUS :
            self.x = 0+self.RADIUS+1
            self.vx = -self.e*self.vx_new 
        elif self.x > SCREEN_WIDTH-self.RADIUS-1:
            self.x = SCREEN_WIDTH-self.RADIUS
            self.vx = -self.e*self.vx_new
        else:
            self.vx = self.vx_new
          
            
        #var = sp.symbols('var')
        #equation = (-(self.rho * self.area * self.cd * delta_time) / (2 * self.mass)) * (var ** 2) * np.sign(self.vy) - var + self.vy - self.g * delta_time
        #self.vy_new = sp.solve(equation, var)
        alpha = (self.rho * self.area * self.cd * delta_time) / (2 * self.mass) * np.sign(self.vy)
        if self.vy == 0:
            self.vy_new = 0
        else:
            self.vy_new = [(1 + math.sqrt(1+4*alpha*(self.vy-self.g*delta_time)))/(-2*alpha)]
            self.vy_new.append((1 - math.sqrt(1+4*alpha*(self.vy-self.g*delta_time)))/(-2*alpha))
            self.vy_new = np.asarray(self.vy_new)
            self.vy_new = self.vy_new.flat[np.abs(self.vy_new - self.vy).argmin()]
        self.ay = (self.vy_new - self.vy) / delta_time
        self.y += self.vy_new * delta_time * 2
        
        if self.y < 0+self.RADIUS:
            self.y = 0+self.RADIUS+1
            self.vy = -self.e*self.vy_new
        elif self.y > SCREEN_HEIGHT-self.RADIUS:
            self.y = SCREEN_HEIGHT-self.RADIUS-1
            self.vy = -self.e*self.vy_new
        else:
            self.vy = self.vy_new
            
        for wall in BASKET:
            if self.collide_with_basket(wall):
                # Reflect ball's speed based on the wall's orientation
                if wall[0][0] == wall[1][0]:  # Vertical wall
                    self.vx = -self.vx*0.5
                else:  # Horizontal wall
                    self.vy = -self.vy*0.5
                    
        if BASKET[0][0][0]+self.RADIUS < self.x < BASKET[2][0][0]+self.RADIUS and BASKET[1][0][1]+self.RADIUS < self.y < BASKET[1][1][1]+self.RADIUS:
            self.vx=0
            self.vy=0
                    
                    
    def collide_with_basket(self, wall):
        """Check if the ball collides with a wall segment."""
        # Wall segment endpoints
        x1, y1 = wall[0]
        x2, y2 = wall[1]

        # Line segment formula to find the distance from the ball to the wall
        num = abs((y2 - y1) * self.x - (x2 - x1) * self.y + x2 * y1 - y2 * x1)
        den = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        dist = num / den

        # Check if the ball is within the RADIUS distance to the wall segment
        if dist < self.RADIUS+2:
            # Further check if the ball's center is within the wall segment's bounds
            if min(x1, x2) - self.RADIUS+2 <= self.x <= max(x1, x2) + self.RADIUS-2 and min(y1, y2) - self.RADIUS+2 <= self.y <= max(y1, y2) + self.RADIUS-2:
                return True
        return False
    
    def reset(self):
        """Reset the ball's position and velocity."""
        self.x = self.initial_x
        self.y = self.initial_y
        self.vx = 0
        self.vy = 0
    
    

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Configuration")
        self.parameters = {
            "Mass": 300,
            "Drag Coefficient": 0.47,
            "Area": 1,
            "Air Density": 1.15,
            "Gravity": 9.81 * 50
        }
        self.sliders = {}
        self.create_sliders()

    def create_sliders(self):
        row = 0
        for key, value in self.parameters.items():
            label = tk.Label(self.root, text=key)
            label.grid(row=row, column=0, padx=10, pady=10)
            slider = tk.Scale(self.root, from_= 1, to=value * 2, orient=tk.HORIZONTAL)
            slider.set(value)
            slider.grid(row=row, column= 1, padx=10, pady=10)
            self.sliders[key] = slider
            row += 1

        save_button = tk.Button(self.root, text="Save", command=self.save_config)
        save_button.grid(row=row, columnspan=2, padx=10, pady=10)

    def save_config(self):
        config = {key: slider.get() for key, slider in self.sliders.items()}
        with open("config.txt", "w") as file:
            file.write(str(config))
        messagebox.showinfo("Configuration Saved", "Configuration has been saved successfully!")
        self.root.destroy()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()
