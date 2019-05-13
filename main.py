
import arcade

from spaceman.core import window
# from .settings import get_setting

def main():
    # resolution = get_setting("resolution")
    game = window.Spaceman(1000, 600, "Space Stuff")
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
