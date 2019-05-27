"""
The physical home base of the player.

Here, we have an evolution process that takes place as the user
upgrades their equipment, station, ships, and defense.
"""
extends Node2D

# -- Imports
const StarGate = preload("res://scenes/objects/StarGate_Small.tscn");

# -- Members
var _stargate;
var _station;

func from_json(data: Dictionary):
    """
    Boot the home base from our json data
    """
    _stargate.boot(data.get("stargate", "alpha"));
    _station.from_json(data.get("station", {}));

func _ready():
    # -- Boot up our StarGate
    var sg_root = $StargateLocation;
    _stargate = StarGate.instance();
    sg_root.add_child(_stargate);
    _station = $PlayerStation;
