import arcade
import random

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Logistics Tetris"

class Box:
    count = 1

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.selected = False
        self.color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        self.BOX_SIDE = 20
        self.BOX_SIZE = random.randint(1, 3)*self.BOX_SIDE
        self.name = str(Box.count)
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
                    arcade.draw_text(self.name, self.x-7, self.y-7, arcade.color.WHITE, font_size=15)
        else:
            #arcade.draw_rectangle_outline(self.x, self.y, self.BOX_SIZE, self.BOX_SIZE, arcade.color.WHITE)
            for x in range(GRID_COUNT_X):
                for y in range(GRID_COUNT_Y):
                    grid_x = self.BOX_LEFT + x * self.BOX_SIDE + self.BOX_SIDE // 2
                    grid_y = self.BOX_BOTTOM + y * self.BOX_SIDE + self.BOX_SIDE // 2
                    arcade.draw_rectangle_filled(grid_x, grid_y, self.BOX_SIDE - 2, self.BOX_SIDE - 2, self.color)
                    arcade.draw_text(self.name, self.x-7, self.y-7, arcade.color.WHITE, font_size=15)


class LogisticsTetris(arcade.View):
    
    def __init__(self):

        super().__init__()
        self.boxes = [Box(SCREEN_WIDTH/2, (5/6)*SCREEN_HEIGHT)]
        self.square_x = 20  # Starting position for the square (x-coordinate)
        self.square_y = 20  # Starting position for the square (y-coordinate)
        wall_width=210
        wall_height=10

        # Define the walls as rectangles (x, y, width, height)
        self.walls = [
            (SCREEN_WIDTH/2, (SCREEN_HEIGHT-wall_width)/2, wall_width+10, wall_height),
            ((SCREEN_WIDTH+wall_width)/2, SCREEN_HEIGHT/2, wall_height, wall_width+10),
            (SCREEN_WIDTH/2, (SCREEN_HEIGHT+wall_width)/2, wall_width+10, wall_height)]
        
        self.keys_pressed = {}
        self.selected_index = 0
        self.background = arcade.load_texture("AI Game jam BG.jpg")
        self.bg_scale = self.background.width / SCREEN_WIDTH  # Calculate the scaling factor\
        self.requested_box = None

        self.delivered = 0
        self.spawned = 0
        self.initial_req = False

        self.timer = 30
        self.spawning_enabled = True
        self.spawn_timer = 10
        #self.schedule_spawn()


    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture("AI Game jam BG.jpg")
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        for Box in self.boxes:
            Box.draw()
        for wall in self.walls:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.RED)
        arcade.draw_rectangle_outline(20, 450, 50, 50, arcade.color.WHITE)
        if self.requested_box is not None:
            req = 'Box' + self.requested_box.name
            arcade.draw_text(req, 400, 400, arcade.color.WHITE, font_size=15)
        delivery_text= 'Delivered ' + str(self.delivered) + ' boxes'
        arcade.draw_text(delivery_text, 400, 450, arcade.color.WHITE, font_size = 15)
        arcade.draw_text(f"Timer: {self.timer:.1f}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, font_size=14)


    def on_mouse_press(self, x, y, button, modifiers):
        # Check if any circle was clicked, and set it as selected
        for index, box in enumerate(self.boxes):
            if abs(x - box.x) < box.BOX_SIZE and abs(y - box.y) < box.BOX_SIZE:
                self.selected_index = index
                break

    def on_key_press(self, key, modifiers):
        # Add the pressed key to the dictionary with a value of True
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
            self.spawning_enabled = False
        else:
            self.keys_pressed[key] = True       
        

    def on_key_release(self, key, modifiers):
        # Remove the released key from the dictionary
        if key in self.keys_pressed:
            del self.keys_pressed[key]

    def on_update(self, delta_time):
        # Move the selected box using the arrow keys

        for box in self.boxes:
            box.selected = False

        if self.selected_index is not None:
            selected_box = self.boxes[self.selected_index]
            selected_box.selected = True
            self.otherboxes=self.boxes.copy()
            self.otherboxes.remove(selected_box)


        new_x = selected_box.x
        new_y = selected_box.y

        if arcade.key.LEFT in self.keys_pressed:
            new_x -= 5
        if arcade.key.RIGHT in self.keys_pressed:
            new_x += 5
        if arcade.key.UP in self.keys_pressed:
            new_y += 5
        if arcade.key.DOWN in self.keys_pressed:
            new_y -= 5
        
        for wall in self.walls:
            if new_x + selected_box.BOX_SIZE/2 > wall[0] -wall[2]/2 and new_x - selected_box.BOX_SIZE/2 < wall[0] + wall[2]/2 and \
                    new_y + selected_box.BOX_SIZE/2 > wall[1] - wall[3]/2 and new_y - selected_box.BOX_SIZE/2 < wall[1] + wall[3]/2:
                
                # If there's a collision, do not update the square's position
                return
            
        for box in self.otherboxes:
            if new_x + selected_box.BOX_SIZE/2 > box.x-box.BOX_SIZE/2 and new_x - selected_box.BOX_SIZE/2 < box.x+box.BOX_SIZE/2 and \
                    new_y + selected_box.BOX_SIZE/2 > box.y-box.BOX_SIZE/2 and new_y - selected_box.BOX_SIZE/2 < box.y+box.BOX_SIZE/2:
                
                # If there's a collision, do not update the square's position
                return
        # Check if the new position is within the boundary of the screen
        if new_x - selected_box.BOX_SIZE/2 < 0:
            new_x = selected_box.BOX_SIZE/2
        elif new_x + selected_box.BOX_SIZE/2 > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - selected_box.BOX_SIZE/2
        if new_y - selected_box.BOX_SIZE/2 < 0:
            new_y = selected_box.BOX_SIZE/2
        elif new_y + selected_box.BOX_SIZE/2 > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - selected_box.BOX_SIZE/2

        if self.spawned == 5 and not self.initial_req:
            self.request_box()
            self.initial_req = True

        if self.requested_box is not None:
            if selected_box.name == self.requested_box.name and abs(new_x - 20) < selected_box.BOX_SIZE and abs(new_y - 450) < selected_box.BOX_SIZE:
                print('YES!')
                self.boxes.remove(selected_box)
                self.selected_index = 0
                self.delivered += 1
                self.request_box()
                self.timer += 10
                

        selected_box.x = new_x
        selected_box.y = new_y

        if self.window.current_view == self:
            self.timer -= delta_time
            self.spawn_timer += delta_time

        if self.spawning_enabled and self.spawn_timer >= 10:
            self.spawn_box()
            self.spawn_timer = 0

    def spawn_box(self):
        self.boxes.append(Box(300, 400))
        self.spawned += 1

    def request_box(self):
        self.requested_box = self.boxes[random.randint(0, len(self.boxes)-1)]
        print(self.requested_box.name)


class StartScreen(arcade.View):

    def __init__(self):

        super().__init__()
        self.start_text = ['Welcome to Block Master, a tetris inspired space optimization game.', 
            'Try to keep the boxes spawned within the warehouse and deliver them as required.',
            'Every box delivered gives you a time boost. Once you run out of time, you lose.']
       
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text(self.start_text[0], SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40, arcade.color.BLACK, font_size = 20, anchor_x="center", anchor_y="center")
        arcade.draw_text(self.start_text[1], SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10, arcade.color.BLACK, font_size = 20, anchor_x="center", anchor_y="center")
        arcade.draw_text(self.start_text[2], SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20, arcade.color.BLACK, font_size = 20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)
            self.window.game_view.spawning_enabled = True
            self.window.game_view.schedule_spawn()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.menu_view = StartScreen()
    window.game_view = LogisticsTetris()
    window.show_view(window.menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
