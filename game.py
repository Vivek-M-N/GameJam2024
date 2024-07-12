import arcade
import math
import numpy
import sympy as sp

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"
GRAVITY = 9.8  # Gravity constant

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        # self.background = arcade.load_texture("AI Game jam BG.jpg")
        # self.bg_scale = self.background.width / SCREEN_WIDTH
        self.ball = Circle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.mouse_pressed = False
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0
        
        wall_width=10
        wall_height=10
        
        self.walls = [
            (SCREEN_WIDTH-120, SCREEN_HEIGHT/2, wall_width, 100),
            (SCREEN_WIDTH-70, SCREEN_HEIGHT/2-50, 100, wall_height),
            (SCREEN_WIDTH-20, SCREEN_HEIGHT/2, wall_width, 100)]

    def on_draw(self):
        arcade.start_render()
        # arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0))
        self.ball.draw()
        if self.mouse_pressed:
            arcade.draw_line(self.ball.x, self.ball.y, self.current_x, self.current_y, arcade.color.WHITE)
            self.draw_trajectory(self.ball.x, self.ball.y, self.current_x, self.current_y)
            
        for wall in self.walls:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.ALLOY_ORANGE)
            
    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pressed = True
        self.start_x = x
        self.start_y = y


    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self.current_x = x
            self.current_y = y

    def draw_trajectory(self, start_x, start_y, current_x, current_y):
        velocity_x = (start_x - current_x) / 2  # Adjust scaling factor as needed
        velocity_y = (start_y - current_y) / 2  # Adjust scaling factor as needed
        
        for t in range(1, 100):  # Increase range for a longer trajectory
            t /= 10  # Scale time down
            self.end_x = start_x + velocity_x * t
            self.end_y = start_y + velocity_y * t - 0.5 * GRAVITY * t ** 2
            
            if self.end_y < self.ball.RADIUS or self.end_y > SCREEN_HEIGHT-self.ball.RADIUS or self.end_x < self.ball.RADIUS or self.end_x > SCREEN_WIDTH-self.ball.RADIUS :  # Stop if it hits the ground
                break

            arcade.draw_circle_filled(self.end_x, self.end_y, 2, arcade.color.YELLOW)
            
    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = False
        self.ball.calculate_x()
        self.ball.calculate_y()
                
class Circle:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
        self.color = (255, 0, 0)
        self.RADIUS = 30
        self.name = str(Circle.count)
        self.mass = 300 #arbitrary values for now
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
        equation = ((self.rho*self.area*self.cd*self.timestep)/(2*self.mass))*(var**2) - var + self.vx
        self.vx_new = sp.solve(equation, var)
        self.vx_new = self.vx_new[self.vx_new != 0]
        print(self.vx_new)
        self.ax=(self.vx_new-self.vx)/self.timestep
        self.x+=self.vx*self.timestep + (self.ax*(self.timestep**2))/2
        print(self.x)

    def calculate_y(self):
        var = sp.symbols('var')
        equation = ((self.rho*self.area*self.cd*self.timestep)/(2*self.mass))*(var**2) - var + self.vy + self.g*self.timestep
        self.vy_new = sp.solve(equation, var)
        self.vy_new = self.vy_new[self.vy_new != 0]
        print(self.vy_new)
        self.ay=(self.vy_new-self.vy)/self.timestep
        self.y+=self.vy*self.timestep + (self.ay*(self.timestep**2))/2
        print(self.y)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.game_view = GameView()
    window.show_view(window.game_view)
    arcade.run()

if __name__ == "__main__":
    main()