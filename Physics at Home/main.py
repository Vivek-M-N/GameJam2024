import arcade
import os
import pygame
from tkinter import messagebox
import tkinter as tk
from config_app import ConfigApp
from levels.level1 import Level1

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"

class Start(arcade.View):
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.background = arcade.load_texture("assets/title page.png")
        self.bg_scale = self.background.width / SCREEN_WIDTH
        self.main_menu = MainMenu()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Press P to play", 700, 130, arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.window.show_view(self.main_menu)
            
    def on_mouse_press(self, x, y, button, modifiers):
         self.mouse_pressed = True

    def on_mouse_release(self, x, y, button, modifiers):
         self.mouse_pressed = False
         self.mouse_released = True
         self.window.show_view(self.main_menu)
         

class MainMenu(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Press P to Play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press E to Experiment", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press R to Reset", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
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
    start = Start(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show_view(start)
    arcade.run()

if __name__ == "__main__":
    if os.path.exists("config.txt"):
        os.remove("config.txt")
    main()
