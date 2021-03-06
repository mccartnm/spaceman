
import arcade

from . import inventory
from .ship import Ship
from .utils import Position
from .damage import Damage
from .tobject import TObject, TSignal

class Player(TObject):
    """
    The player itself!
    """

    def __init__(self):
        super().__init__()

        self._ship = None
        self._inventory = inventory.PlayerInventory()

        # Are we allowed to control the ship?
        self._can_control = True

        # Mapping to help with key release management
        self._pressed_keys = set()

    @property
    def ship(self):
        return self._ship

    def update(self, delta_time):
        """
        Update the players game state
        """
        if self._ship:
            self.ship.update(delta_time)

    def set_ship(self, ship: Ship):
        """
        Set the players active ship
        """
        if self._ship:
            self._ship.stop_listening(self.ship_took_damage)

        self._ship = ship
        self._ship.take_damage.listen_post(
            self.ship_took_damage
        )

        # To reset any interfaces
        self.ship_took_damage(Damage('null'))

    @TSignal
    def ship_took_damage(self, damage: Damage):
        """
        A player takes damage whenever they're hit by an
        ememy projectile
        
        - For the moment, this is just for others to listen to
        without the need to extend a connection to each ship
        if the player changes said ship
        """
        pass

    def on_key_press(self, key, modifiers):
        """
        Whenever we press a key, we see if the user has any
        reason to need it.
        :return: Boolean - True is we've consumed the input
        """
        if not self.ship or not self._can_control:
            return False

        """
        W - Thrust Forward
        S - Thrust Backward
        A - Turn Left
        D - Turn right
        Q - Strafe Left
        E - Strafe Right
        """
        consumed = True
        self._pressed_keys.add(key)

        if key == arcade.key.W:
            self.ship.set_thrust(self.ship.thrust + Position(0, 0.15))
        elif key == arcade.key.S:
            self.ship.set_thrust(self.ship.thrust + Position(0, -0.15))
        elif key == arcade.key.Q:
            self.ship.set_thrust(self.ship.thrust + Position(0.1, 0))
        elif key == arcade.key.E:
            self.ship.set_thrust(self.ship.thrust + Position(-0.1, 0))
        elif key == arcade.key.A:
            self.ship.set_angle_delta(self.ship.angle_delta + 3)
        elif key == arcade.key.D:
            self.ship.set_angle_delta(self.ship.angle_delta - 3)

        # Fire/Utility Controls
        elif key == arcade.key.SPACE:
            self.ship.fire_command('fire1')
        elif key >= arcade.key.KEY_1 and key <= arcade.key.KEY_9:
            self.ship.fire_command(f'util{key - arcade.key.KEY_0}')

        elif key == arcade.key.I:
            self.ship.take_damage(Damage(Damage.PIERCE, 100))

        else:
            consumed = False

        return consumed

    def on_key_release(self, key, modifiers):
        """
        Whenever we release a key - make sure to augment the
        player accordingly
        """
        if not self.ship or not self._can_control:
            return False

        self._pressed_keys.remove(key)

        consumed = True

        if key == arcade.key.W:
            self.ship.set_thrust(self.ship.thrust - Position(0, 0.15))
        elif key == arcade.key.S:
            self.ship.set_thrust(self.ship.thrust - Position(0, -0.15))
        elif key == arcade.key.Q:
            self.ship.set_thrust(self.ship.thrust - Position(0.1, 0))
        elif key == arcade.key.E:
            self.ship.set_thrust(self.ship.thrust - Position(-0.1, 0))
        elif key == arcade.key.A:
            self.ship.set_angle_delta(self.ship.angle_delta - 3)
        elif key == arcade.key.D:
            self.ship.set_angle_delta(self.ship.angle_delta + 3)
        else:
            consumed = False

        if len(self._pressed_keys) == 0:
            self.ship.set_angle_delta(0.0)
            self.ship.set_thrust(Position(0.0, 0.0))

        return True