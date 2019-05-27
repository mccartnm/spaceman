"""
Campaign tools for building/managing campaigns!
"""

extends Node

# -- Imports
const Player = preload("player.gd");
const Space  = preload("res://scenes/space.tscn");
const Stats  = preload("res://scenes/interface/Stats.tscn");
const Active = preload("res://scenes/interface/ActiveItems.tscn");

const Home = preload("res://scenes/campaign/Home.tscn");

func _init_player_interface():
    """
    Build the players interface setup
    """
    var r = get_node("/root/GAME/ui");
#    var stats = Stats.instance();
#    r.add_child(stats);
    var items = Active.instance();
    r.add_child(items);


func player_start(player: Player):
    """
    Development starter pack
    """
    var r = get_node("/root/GAME");

    var ship = PrototypeLoader.SHIPS.new_ship("Skalk", Vector2(0, 0));
    ship.set_z_index(0);
    ship.follow();
    player.set_ship(ship);

    r.add_child(Space.instance()); #< Give us some space love
    r.add_child(ship);        #< Bring the ship up (Move this)

    var home_base = Home.instance();
    r.add_child(home_base);

    # -- Once we have our home base added to the
    # world - it's time to 
    home_base.from_json({
        "stargate" : "alpha"
    });

func _ready():
    _init_player_interface();
