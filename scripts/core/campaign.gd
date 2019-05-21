"""
Campaign tools for building/managing campaigns!
"""

extends Node

# -- Imports
const Player = preload("player.gd");
const Space = preload("space.gd");

func _basic_start(player: Player):
    """
    Development starter pack
    """
    var r = get_node("/root/GAME");

    var ship = PrototypeLoader.SHIPS.new_ship("Skalk", Vector2(250, 250));
    ship.set_z_index(0);
    player.set_ship(ship);

    r.add_child(Space.new()); #< Give us some space love
    r.add_child(ship);        #< Bring the ship up (Move this)

func _ready():
    pass
