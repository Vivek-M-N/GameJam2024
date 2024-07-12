import arcade
import math

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
            (500, (SCREEN_HEIGHT-wall_width)/2, wall_width+10, wall_height),
            (500, (SCREEN_HEIGHT)/2, wall_width+10, wall_height),
            (500, (SCREEN_HEIGHT+wall_width)/2, wall_width+10, wall_height)]

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

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = False
        self.ball.x = x
        self.ball.y = y

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self.current_x = x
            self.current_y = y

    def draw_trajectory(self, start_x, start_y, current_x, current_y):
        velocity_x = (start_x - current_x) / 10  # Adjust scaling factor as needed
        velocity_y = (start_y - current_y) / 10  # Adjust scaling factor as needed
        
        for t in range(1, 100):  # Increase range for a longer trajectory
            t /= 10  # Scale time down
            new_x = start_x + velocity_x * t
            new_y = start_y + velocity_y * t - 0.5 * GRAVITY * t ** 2
            
            if new_y < 0:  # Stop if it hits the ground
                break

            arcade.draw_circle_filled(new_x, new_y, 2, arcade.color.YELLOW)

class Circle:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
        self.color = (255, 0, 0)
        self.RADIUS = 30
        self.name = str(Circle.count)
        Circle.count += 1

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.RADIUS, self.color)
        arcade.draw_text(self.name, self.x - 7, self.y - 7, arcade.color.WHITE, font_size=15)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.game_view = GameView()
    window.show_view(window.game_view)
    arcade.run()

if __name__ == "__main__":
    main()
