"""
Mount point for a ship hardpoint
"""
extends Node2D

signal hardpoint_changed;

const Hardpoint = preload("../hardpoint.gd");

var _info: Dictionary;
var _ship;
var _hardpoint: Hardpoint;

func _init(info: Dictionary, ship):
    _info = info;
    _ship = ship;
    
    _hardpoint = null;
    if (default()):
        set_hardpoint(PrototypeLoader.HARDPOINTS.new_hardpoint(
            default(),
            _info,
            _ship
        ));
    
    _ship.add_child(self);
    set_position(location());

func set_hardpoint(hp: Hardpoint):
    if _hardpoint:
        remove_child(_hardpoint);
    _hardpoint = hp;
    emit_signal("hardpoint_changed");
    add_child(_hardpoint);

func default() -> String:
    return _info["default"];
    
func command() -> String:
    return _info["command"];

func hardpoint():
    return _hardpoint;

func location() -> Vector2:
#    var hardpoint_center = _hardpoint.get_current_size() / 2;
    var ship_center = _ship.get_current_size() / 2;

    var this_location = Vector2(
        _info["location"][0],
        _info["location"][1]
    );
    
    var relative_location = this_location - ship_center;
    return relative_location;

func fire():
    """
    Fire this hardpoint
    """
    return _hardpoint.fire();