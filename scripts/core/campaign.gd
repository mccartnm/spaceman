"""
Campaign tools for building/managing campaigns!
"""

extends Node

# -- Imports
const Player = preload("player.gd");
const Space  = preload("space.gd");
const Stats  = preload("res://scenes/interface/Stats.tscn");
const Active = preload("res://scenes/interface/ActiveItems.tscn");

const Aster = preload("res://scenes/objects/Asteroid_Small.tscn");

func _init_player_interface():
    """
    Build the players interface setup
    """
    var r = get_node("/root/GAME/ui");
#    var stats = Stats.instance();
#    r.add_child(stats);

    var items = Active.instance();
    r.add_child(items);

func _basic_start(player: Player):
    """
    Development starter pack
    """
    var r = get_node("/root/GAME");

    var ship = PrototypeLoader.SHIPS.new_ship("Lamella", Vector2(0, 0));
    ship.set_z_index(0);
    ship.follow();
    player.set_ship(ship);

    r.add_child(Space.new()); #< Give us some space love
    r.add_child(ship);        #< Bring the ship up (Move this)

    _init_player_interface();

func _ready():
    pass
