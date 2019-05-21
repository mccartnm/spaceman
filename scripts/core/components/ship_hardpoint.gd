"""
Mount point for a ship hardpoint
"""
extends Node

var _info: Dictionary;
var _ship;
var _hardpoint;

func _init(info: Dictionary, ship):
    _info = info;
    _ship = ship;
    
    _hardpoint = null;
    if (default()):
        _hardpoint = PrototypeLoader.HARDPOINTS.new_hardpoint(
            default(),
            _info,
            _ship
        );

func default() -> String:
    return _info["default"];

func hardpoint():
    return _hardpoint;