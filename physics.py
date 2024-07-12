import arcade
import numpy
import sympy as sp 

class Circle:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
        self.color = (255, 0, 0)
        self.RADIUS = 30
        self.name = str(Circle.count)
        self.mass = 50 #arbitrary values for now
        self.cd = 0.47
        self.area = 1
        self.rho = 1.82
        self.force = 50
        self.theta = 20
        self.timestep = 0.01666
        self.g=9.81
        self.vx=0
        self.vx_new=0 
        self.vy=0
        self.vy_new=0
        self.ax=0
        self.ay=0
        Circle.count += 1

    def draw(self):
        
        arcade.draw_circle_filled(self.x, self.y, self.RADIUS, self.color)
        arcade.draw_text(self.name, self.x - 7, self.y - 7, arcade.color.WHITE, font_size=15)

    def calculate_x(self):
        var = sp.symbols('var')
        ((self.rho*self.area*self.cd*self.timestep)/(2*self.mass))*(var**2) - var + self.vx == 0 
        self.vx_new = sp.solve(equation, var)
        self.ax=(self.vx_new-self.vx)/self.timestep
        self.x=self.vx*self.timestep + (self.ax*(self.timestep**2))/2

    def calculate_y(self):
        var = sp.symbols('var')
        ((self.rho*self.area*self.cd*self.timestep)/(2*self.mass))*(var**2) - var + self.vy + self.g*self.timestep  == 0
        self.vy_new = sp.solve(equation, var)
        self.ay=(self.vy_new-self.vy)/self.timestep
        self.y=self.vy*self.timestep + (self.ay*(self.timestep**2))/2