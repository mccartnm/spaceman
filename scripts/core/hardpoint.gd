"""
A weapon or utility of a vessel
"""
extends Node

# -- Imports

# -- Members
var _info: Dictionary;
var _ship_info: Dictionary;
var _ship;

func _init(hp_info: Dictionary, ship_hp_info: Dictionary, ship):
    """
    Initialize the Node
    """
    _info = hp_info;
    _ship_info = ship_hp_info;
    _ship = ship;