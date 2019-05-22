"""
A weapon or utility of a vessel

TODO: Add other types and properties
"""
extends Node2D

# -- Imports
const Bullet = preload("../../scenes/projectile/bullet_function.tscn");

# -- Members
var _info: Dictionary;
var _ship_info: Dictionary;
var _ship;

# Additional tools
var _on: bool = false;
var _tick: float = 0.0;

func _init(hp_info: Dictionary, ship_hp_info: Dictionary, ship):
    """
    Initialize the Node
    """
    _info = hp_info;
    _ship_info = ship_hp_info;
    _ship = ship;

func type() -> String:
    return _info["type"];
    
func damage():
    return _info["damage"];

func range_():
    return _info["range"];

func props() -> Dictionary:
    return _info["props"];

func rate():
    return _info["rate"];

func fire():
    match type():
        PrototypeLoader.HARDPOINTS.BULLET:
            var p = props();
            if p.get('automatic', false):
                _on = true;
                _tick = 0.0;
                _fire();
            else:
                _fire();

func release():
    """
    We are no longer holding down this command
    """
    match type():
        PrototypeLoader.HARDPOINTS.BULLET:
            _on = false;

func _fire():
    var root_node = get_node("/root/GAME");
    if type() == PrototypeLoader.HARDPOINTS.BULLET:
        var bullet = Bullet.instance()
        bullet.start(
            props().get('sprite', 'basic_bullet'),
            damage(),
            global_position,
            range_(),
            get_parent()
        );
        root_node.add_child(bullet);

func _physics_process(delta):
    """
    Check if we have to process firing our weapon
    """
    if not _on:
        return # Nothing to do

    _tick += delta;

    match type():
        PrototypeLoader.HARDPOINTS.BULLET:
            if _tick > (1.0 / float(rate())):
                _tick = 0;
                _fire();
