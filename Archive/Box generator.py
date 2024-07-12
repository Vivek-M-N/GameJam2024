import arcade
import random

# Constants for the screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Box with Gridlines and Random Colors"

class Box:
    count = 1

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.selected = False
        self.color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        self.BOX_SIDE = 20
        self.BOX_SIZE = random.randint(1, 3)*self.BOX_SIDE
        self.name = "Box "+ str(Box.count)
        Box.count += 1

    def draw(self):

         # Constants for the box
        self.BOX_LEFT = self.x - self.BOX_SIZE // 2
        self.BOX_RIGHT = self.BOX_LEFT + self.BOX_SIZE
        self.BOX_BOTTOM = self.y - self.BOX_SIZE // 2
        self.BOX_TOP = self.BOX_BOTTOM +self.BOX_SIZE

        # Constants for the grid
        GRID_COUNT_X = self.BOX_SIZE // self.BOX_SIDE
        GRID_COUNT_Y = self.BOX_SIZE // self.BOX_SIDE

        if self.selected:
            arcade.draw_rectangle_outline(self.x, self.y, self.BOX_SIZE, self.BOX_SIZE, arcade.color.WHITE)
            for x in range(GRID_COUNT_X):
                for y in range(GRID_COUNT_Y):
                    grid_x = self.BOX_LEFT + x * self.BOX_SIDE + self.BOX_SIDE // 2
                    grid_y = self.BOX_BOTTOM + y * self.BOX_SIDE + self.BOX_SIDE // 2
                    arcade.draw_rectangle_filled(grid_x, grid_y, self.BOX_SIDE - 2, self.BOX_SIDE - 2, self.color)
                    arcade.draw_text(self.name, self.x, self.y, arcade.color.WHITE, font_size=20)
        else:
            #arcade.draw_rectangle_outline(self.x, self.y, self.BOX_SIZE, self.BOX_SIZE, arcade.color.WHITE)
            for x in range(GRID_COUNT_X):
                for y in range(GRID_COUNT_Y):
                    grid_x = self.BOX_LEFT + x * self.BOX_SIDE + self.BOX_SIDE // 2
                    grid_y = self.BOX_BOTTOM + y * self.BOX_SIDE + self.BOX_SIDE // 2
                    arcade.draw_rectangle_filled(grid_x, grid_y, self.BOX_SIDE - 2, self.BOX_SIDE - 2, self.color)
                    arcade.draw_text(self.name, self.x, self.y, arcade.color.WHITE, font_size=20)


class LogisticsTetris(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.boxes = [Box(300, 400), Box(500, 300), Box(0, 300)]
        
    def on_draw(self):
        arcade.start_render()
        for Box in self.boxes:
            Box.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if any circle was clicked, and set it as selected
        for index, box in enumerate(self.boxes):
            if abs(x - box.x) < box.BOX_SIZE and abs(y - box.y) < box.BOX_SIZE:
                self.selected_index = index
                break

    def on_key_press(self, key, modifiers):
        # Move the selected circle using the arrow keys
        for box in self.boxes:
            box.selected = False

        if self.selected_index is not None:
            selected_box = self.boxes[self.selected_index]
            selected_box.selected = True
            if key == arcade.key.LEFT:
                selected_box.x -= 10
            elif key == arcade.key.RIGHT:
                selected_box.x += 10
            elif key == arcade.key.UP:
                selected_box.y += 10
            elif key == arcade.key.DOWN:
                selected_box.y -= 10

def main():
    window = LogisticsTetris()
    arcade.run()

if __name__ == "__main__":
    main()
