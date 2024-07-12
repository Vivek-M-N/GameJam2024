import arcade

# Constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ball toss (but with physics)"

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("AI Game jam BG.jpg")
        self.bg_scale = self.background.width / SCREEN_WIDTH
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #window.menu_view = StartScreen()
    #window.instruction_view = InstructionScreen()
    window.game_view = GameView()
    #window.game_over_view = GameOverScreen()
    window.show_view(window.game_view)
    arcade.run()

if __name__ == "__main__":
    main()
