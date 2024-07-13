import arcade
import os
import numpy as np
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Circle:
    count = 1

    def __init__(self, x, y, windx, windy):
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
        self.windx = windx
        self.windy = windy

        self.texture = arcade.load_texture("assets/ball.png")

        self.load_config()

    def load_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as file:
                config = eval(file.read())
                self.mass = config.get("Mass (kg)", self.mass)
                self.cd = config.get("Drag Coefficient (-)", self.cd)
                self.area = config.get("Area (m^2)", self.area)
                self.rho = config.get("Air Density (kg/m^3)", self.rho)
                self.e = config.get("Coefficient Of Restitution (-)", self.e)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.RADIUS, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.RADIUS * 2, self.RADIUS * 2, self.texture)

    def update(self, delta_time):
        alpha = (self.rho * self.area * self.cd * delta_time) / (2 * self.mass) * np.sign(self.vx)
        b = -1-(self.rho * self.area * self.cd * delta_time * self.windx) / (self.mass) * np.sign(self.vx)
        c = self.vx-(self.rho * self.area * self.cd * delta_time * self.windx**2) / (2 * self.mass) * np.sign(self.vx)
        if self.vx == 0:
            self.vx_new = 0
        else:
            self.vx_new = [(-b + math.sqrt(b**2 + 4*alpha*c))/(-2*alpha)]
            self.vx_new.append((-b - math.sqrt(b**2 + 4*alpha*c))/(-2*alpha))
            self.vx_new = np.asarray(self.vx_new)
            self.vx_new = self.vx_new.flat[np.abs(self.vx_new - self.vx).argmin()]
        self.ax = (self.vx_new - self.vx) / delta_time
        self.x += self.vx_new * delta_time *2
        
        if self.x < 0+self.RADIUS:
            self.x = 0+self.RADIUS+1
            self.vx = -self.e*self.vx_new 
        elif self.x > SCREEN_WIDTH-self.RADIUS-1:
            self.x = SCREEN_WIDTH-self.RADIUS
            self.vx = -self.e*self.vx_new
        else:
            self.vx = self.vx_new
          
        alpha = (self.rho * self.area * self.cd * delta_time) / (2 * self.mass) * np.sign(self.vy)
        b = -1-(self.rho * self.area * self.cd * delta_time * self.windy) / (self.mass) * np.sign(self.vy)
        c = self.vy-(self.rho * self.area * self.cd * delta_time * self.windy**2) / (2 * self.mass) * np.sign(self.vy) - self.g*delta_time
        if self.vy == 0:
            self.vy_new = 0
        else:
            self.vy_new = [(-b + math.sqrt(b**2 + 4*alpha*c))/(-2*alpha)]
            self.vy_new.append((-b - math.sqrt(b**2 + 4*alpha*c))/(-2*alpha))
            self.vy_new = np.asarray(self.vy_new)
            self.vy_new = self.vy_new.flat[np.abs(self.vy_new - self.vy).argmin()]
        self.ay = (self.vy_new - self.vy) / delta_time
        self.y += self.vy_new * delta_time *2  
        
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
