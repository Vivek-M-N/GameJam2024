import arcade

# Constants for the screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Move the Square with Walls and Boundary Box"

# Constants for the square size
SQUARE_SIZE = 20

class SquareGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.square_x = 20  # Starting position for the square (x-coordinate)
        self.square_y = 20  # Starting position for the square (y-coordinate)
        self.keys_pressed = {}  # Dictionary to track keys being held

        # Define the walls as rectangles (x, y, width, height)
        self.walls = [
            (320, 140, 210, 10),
            (420, 240, 10, 205),
            (320, 340, 210, 10)
            # Add more walls here if needed
        ]

    def on_draw(self):
        arcade.start_render()
        # Draw the walls
        for wall in self.walls:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.RED)
        # Draw the square at its current position
        arcade.draw_rectangle_filled(self.square_x, self.square_y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.BLUE)

    def on_key_press(self, key, modifiers):
        # Add the pressed key to the dictionary with a value of True
        self.keys_pressed[key] = True

    def on_key_release(self, key, modifiers):
        # Remove the released key from the dictionary
        if key in self.keys_pressed:
            del self.keys_pressed[key]

    def on_update(self, delta_time):
        # Calculate the potential new position of the square
        new_square_x = self.square_x
        new_square_y = self.square_y

        # Update the square's position if the arrow keys are held
        if arcade.key.LEFT in self.keys_pressed:
            new_square_x -= 5
        if arcade.key.RIGHT in self.keys_pressed:
            new_square_x += 5
        if arcade.key.UP in self.keys_pressed:
            new_square_y += 5
        if arcade.key.DOWN in self.keys_pressed:
            new_square_y -= 5

        # Check if the new position collides with any walls
        for wall in self.walls:
            if new_square_x + SQUARE_SIZE/2 > wall[0] -wall[2]/2 and new_square_x - SQUARE_SIZE/2 < wall[0] + wall[2]/2 and \
                    new_square_y + SQUARE_SIZE/2 > wall[1] - wall[3]/2 and new_square_y - SQUARE_SIZE/2 < wall[1] + wall[3]/2:
                # If there's a collision, do not update the square's position
                return

        # Check if the new position is within the boundary of the screen
        if new_square_x - SQUARE_SIZE/2 < 0:
            new_square_x = SQUARE_SIZE/2
        elif new_square_x + SQUARE_SIZE/2 > SCREEN_WIDTH:
            new_square_x = SCREEN_WIDTH - SQUARE_SIZE/2
        if new_square_y - SQUARE_SIZE/2 < 0:
            new_square_y = SQUARE_SIZE/2
        elif new_square_y + SQUARE_SIZE/2 > SCREEN_HEIGHT:
            new_square_y = SCREEN_HEIGHT - SQUARE_SIZE/2

        # Update the square's position if there is no collision with walls and within the screen boundary
        self.square_x = new_square_x
        self.square_y = new_square_y

def main():
    window = SquareGame()
    arcade.run()

if __name__ == "__main__":
    main()