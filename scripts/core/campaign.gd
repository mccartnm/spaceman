"""
Campaign tools for building/managing campaigns!
"""

extends Node

# -- Imports
const Player = preload("player.gd");
const Space  = preload("res://scenes/space.tscn");
const Stats  = preload("res://scenes/interface/Stats.tscn");
const Active = preload("res://scenes/interface/ActiveItems.tscn");

const StarGate = preload("res://scenes/objects/StarGate_Small.tscn");

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

    var ship = PrototypeLoader.SHIPS.new_ship("Skalk", Vector2(0, 0));
    ship.set_z_index(0);
    ship.follow();
    player.set_ship(ship);

    var sg = StarGate.instance();
    sg.boot("alpha");
    sg.global_position = Vector2(-400, -1000);
    r.add_child(sg);

    r.add_child(Space.instance()); #< Give us some space love
    r.add_child(ship);        #< Bring the ship up (Move this)

    _init_player_interface();

func _ready():
    pass
