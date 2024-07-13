import arcade
import os
import pygame
from tkinter import messagebox
from config_app import ConfigApp
from levels.level1 import Level1

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"

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
            game_view = Level1(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.window.show_view(game_view)
        elif key == arcade.key.E:
            root = tk.Tk()
            app = ConfigApp(root)
            root.mainloop()
            self.window.show_view(self)

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("assets/The Entertainer.mp3")
    pygame.mixer.music.play(-1)  # Play music indefinitely (-1)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    if os.path.exists("config.txt"):
        os.remove("config.txt")
    main()
