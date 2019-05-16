
import arcade

from spaceman.core import window
from spaceman.core.settings import get_setting, set_setting

set_setting('global_scale', 1.0)
set_setting('resolution', (1200, 800))

def main():
    resolution = get_setting('resolution', (1200, 800))
    game = window.Spaceman(*resolution, 'Space Adventures')
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
