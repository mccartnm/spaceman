"""
Engine possible of delivering thrust!
"""
extends "tsprite.gd"

# -- Imports

# -- Members
var _info: Dictionary;
var _engine_info: Dictionary;
var _ship;

func _init(
    eg_info: Dictionary, ship_eg_info: Dictionary, ship
).(
    # -- TSprite Constructor
    PrototypeLoader.engine_directory(),
    AnimationLoadType.Component,
    eg_info["sprite"]
):
    _info = eg_info;
    _engine_info = ship_eg_info;
    _ship = ship;

    _states.set_animation_loop("life-static", true);
    play("life-static");

func power():
    return _info['power'];

func _ready():
    pass