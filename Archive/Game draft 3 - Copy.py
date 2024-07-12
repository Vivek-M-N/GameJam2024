import arcade
import random

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Logistics Tetris"
delivered = 0
total_time = 0
quit_reason = ' '

class Box:
    count = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
        self.color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        self.BOX_SIDE = 20
        self.BOX_SIZE = random.randint(1, 3) * self.BOX_SIDE
        self.name = str(Box.count)
        Box.count += 1

    def draw(self):
        self.BOX_LEFT = self.x - self.BOX_SIZE // 2
        self.BOX_RIGHT = self.BOX_LEFT + self.BOX_SIZE
        self.BOX_BOTTOM = self.y - self.BOX_SIZE // 2
        self.BOX_TOP = self.BOX_BOTTOM + self.BOX_SIZE

        GRID_COUNT_X = self.BOX_SIZE // self.BOX_SIDE
        GRID_COUNT_Y = self.BOX_SIZE // self.BOX_SIDE

        if self.selected:
            arcade.draw_rectangle_outline(self.x, self.y, self.BOX_SIZE, self.BOX_SIZE, arcade.color.WHITE)
        for x in range(GRID_COUNT_X):
            for y in range(GRID_COUNT_Y):
                grid_x = self.BOX_LEFT + x * self.BOX_SIDE + self.BOX_SIDE // 2
                grid_y = self.BOX_BOTTOM + y * self.BOX_SIDE + self.BOX_SIDE // 2
                arcade.draw_rectangle_filled(grid_x, grid_y, self.BOX_SIDE - 2, self.BOX_SIDE - 2, self.color)
                arcade.draw_text(self.name, self.x - 7, self.y - 7, arcade.color.WHITE, font_size=15)

class LogisticsTetris(arcade.View):
    def __init__(self):
        super().__init__()
        self.boxes = [Box(SCREEN_WIDTH / 2, (5 / 6) * SCREEN_HEIGHT)]
        self.square_x = 20
        self.square_y = 20
        wall_width = 350
        wall_height = 10

        self.walls = [
            (500, (SCREEN_HEIGHT - wall_width) / 2, wall_width + 10, wall_height),
            (500, SCREEN_HEIGHT / 2, wall_width + 10, wall_height),
            (500, (SCREEN_HEIGHT + wall_width) / 2, wall_width + 10, wall_height)
        ]

        self.wallsboundary = [
            (403, 80, 645, 5),
            (83, 363, 5, 560),
            (403, 640, 643, 5),
            (723, 363, 5, 560)
        ]

        self.keys_pressed = {}
        self.selected_index = 0
        try:
            self.background = arcade.load_texture("AI Game jam BG.jpg")
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background = None
        
        self.bg_scale = self.background.width / SCREEN_WIDTH if self.background else 1
        self.requested_box = None

        self.spawned = 0
        self.initial_req = False
        self.restart_req = True

        self.timer = 45
        self.spawning_enabled = True
        self.spawn_timer = 0
        self.spawn_duration = 5

    def on_draw(self):
        arcade.start_render()
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        for box in self.boxes:
            box.draw()
        for wall in self.walls:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.ALLOY_ORANGE)
        for wall in self.wallsboundary:
            arcade.draw_rectangle_filled(wall[0], wall[1], wall[2], wall[3], arcade.color.GRAY_BLUE)
        arcade.draw_rectangle_outline(150, 450, 75, 75, arcade.color.SEA_GREEN)
        if self.requested_box:
            req = 'Box' + self.requested_box.name
            arcade.draw_text(req, 740, 440, arcade.color.WHITE, font_size=15)
        delivery_text = 'Delivered ' + str(delivered) + ' boxes'
        arcade.draw_text(delivery_text, 740, 280, arcade.color.WHITE, font_size=15)
        arcade.draw_text(f"Timer: {self.timer:.1f}", 740, 200, arcade.color.RED, font_size=18)

    def on_mouse_press(self, x, y, button, modifiers):
        for index, box in enumerate(self.boxes):
            if abs(x - box.x) < box.BOX_SIZE and abs(y - box.y) < box.BOX_SIZE:
                self.selected_index = index
                break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
            self.spawning_enabled = False
        else:
            self.keys_pressed[key] = True

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            del self.keys_pressed[key]

    def on_update(self, delta_time):
        global quit_reason

        for box in self.boxes:
            box.selected = False

        if self.selected_index is not None:
            selected_box = self.boxes[self.selected_index]
            selected_box.selected = True
            self.otherboxes = self.boxes.copy()
            self.otherboxes.remove(selected_box)

        new_x = selected_box.x
        new_y = selected_box.y

        if arcade.key.A in self.keys_pressed:
            new_x -= 5
        if arcade.key.D in self.keys_pressed:
            new_x += 5
        if arcade.key.W in self.keys_pressed:
            new_y += 5
        if arcade.key.S in self.keys_pressed:
            new_y -= 5

        for wall in self.walls:
            if new_x + selected_box.BOX_SIZE / 2 > wall[0] - wall[2] / 2 and new_x - selected_box.BOX_SIZE / 2 < wall[0] + wall[2] / 2 and \
               new_y + selected_box.BOX_SIZE / 2 > wall[1] - wall[3] / 2 and new_y - selected_box.BOX_SIZE / 2 < wall[1] + wall[3] / 2:
                return

        for wall in self.wallsboundary:
            if new_x + selected_box.BOX_SIZE / 2 > wall[0] - wall[2] / 2 and new_x - selected_box.BOX_SIZE / 2 < wall[0] + wall[2] / 2 and \
               new_y + selected_box.BOX_SIZE / 2 > wall[1] - wall[3] / 2 and new_y - selected_box.BOX_SIZE / 2 < wall[1] + wall[3] / 2:
                return

        for box in self.otherboxes:
            if len(self.boxes) > 1 and abs(self.boxes[-1].x - self.boxes[-2].x) < min(self.boxes[-1].BOX_SIZE, self.boxes[-2].BOX_SIZE) and \
               abs(self.boxes[-1].y - self.boxes[-2].y) < min(self.boxes[-1].BOX_SIZE, self.boxes[-2].BOX_SIZE):
                quit_reason = 'Blocks have stacked up!'
                self.window.show_view(self.window.game_over_view)

            if new_x + selected_box.BOX_SIZE / 2 > box.x - box.BOX_SIZE / 2 and new_x - selected_box.BOX_SIZE / 2 < box.x + box.BOX_SIZE / 2 and \
               new_y + selected_box.BOX_SIZE / 2 > box.y - box.BOX_SIZE / 2 and new_y - selected_box.BOX_SIZE / 2 < box.y + box.BOX_SIZE / 2:
                return

        if new_x - selected_box.BOX_SIZE / 2 < 0:
            new_x = selected_box.BOX_SIZE / 2
        elif new_x + selected_box.BOX_SIZE / 2 > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - selected_box.BOX_SIZE / 2
        if new_y - selected_box.BOX_SIZE / 2 < 0:
            new_y = selected_box.BOX_SIZE / 2
        elif new_y + selected_box.BOX_SIZE / 2 > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - selected_box.BOX_SIZE / 2

        if len(self.boxes) == 5 and not self.initial_req:
            self.request_box()
            self.initial_req = True

        if self.requested_box:
            if selected_box.name == self.requested_box.name and abs(new_x - 150) < 75 / 2 and abs(new_y - 450) < 75 / 2:
                self.timer += 2.5 * selected_box.BOX_SIZE / 20
                self.boxes.remove(self.requested_box)
                self.selected_index = 0
                global delivered
                delivered += 1
                self.request_box()

        selected_box.x = new_x
        selected_box.y = new_y

        if self.window.current_view == self:
            self.timer -= delta_time
            self.spawn_timer += delta_time
            global total_time
            total_time += delta_time

        if self.spawning_enabled and self.spawn_timer >= self.spawn_duration:
            self.spawn_box()
            self.spawn_timer = 0

        if self.timer < 0:
            quit_reason = 'You ran out of time!'
            self.window.show_view(self.window.game_over_view)

    def spawn_box(self):
        self.boxes.append(Box(SCREEN_WIDTH / 2, (5 / 6) * SCREEN_HEIGHT))
        self.spawned += 1

    def request_box(self):
        if len(self.boxes) > 1:
            self.requested_box = self.boxes[random.randint(0, len(self.boxes) - 1)]
        else:
            self.initial_req = False

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()
        try:
            self.background = arcade.load_texture("Blockmaster.png")
        except Exception as e:
            print(f"Error loading start screen background image: {e}")
            self.background = None
        self.bg_scale = self.background.width / SCREEN_WIDTH if self.background else 1

    def on_draw(self):
        arcade.start_render()
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text('Press esc to start and pause', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.instruction_view)

class InstructionScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_text = [
            'Try to keep the boxes spawned within the warehouse and deliver them as required.',
            'Every box delivered gives you a time boost.', 
            'Once you run out of time or let the blocks stack up at the spawn location, You lose',
            'Use the mouse to select boxes and the WASD to move them around'
        ]

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        for i, text in enumerate(self.start_text):
            arcade.draw_text(text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40 - i * 30, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text('Press esc to start and pause', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)
            self.window.game_view.spawning_enabled = True

class GameOverScreen(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.delivered = delivered
        self.total_time = total_time
        self.game_over_text = 'GAME OVER!'
        self.info_text = 'You delivered ' + str(self.delivered) + ' boxes in ' + str(round(self.total_time)) + ' seconds.'
        self.quit_reason = quit_reason
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text(self.game_over_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, arcade.color.BLACK, font_size=40, anchor_x="center", anchor_y="center")
        arcade.draw_text(self.info_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text(self.quit_reason, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.menu_view = StartScreen()
    window.instruction_view = InstructionScreen()
    window.game_view = LogisticsTetris()
    window.game_over_view = GameOverScreen()
    window.show_view(window.menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
