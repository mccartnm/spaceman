"""
Mount point for a ships engine
"""
extends Node2D

signal engine_changed;

# -- Imports
const Engine_ = preload("../engines.gd");

# -- Members
var _info: Dictionary;
var _ship;
var _engine: Engine_;

func _init(info: Dictionary, ship):
    """
    Construct the bitch
    """
    _info = info;
    _ship = ship;

    set_engine(PrototypeLoader.ENGINES.new_engine(
        default(),
        _info,
        _ship
    ));

    _ship.add_child(self);
    set_position(location());

func check_state(thrust: Vector2):
    """
    Based on the direction we're facing, assert if we need to enable
    this engine or not
    :param thrust: Vectory direction of the ship
    """
    match direction():
        's':
            if thrust.y < 0:
                _engine.visible = true;
            else:
                _engine.visible = false;

func set_engine(eg: Engine_):
    """
    Set the engine. This means we may have to move the contact
    point slightly based on the engine requirements
    """
    if _engine:
        remove_child(_engine);
    _engine = eg;
    emit_signal("engine_changed");
    add_child(_engine);

func default() -> String:
    return _info["default"];
    
func direction():
    return _info['direction'];

func engine_size():
    return _info['size']; 

func power():
    return _engine.power();

func location() -> Vector2:
    var engine_center = _engine.get_current_size() / 2;
    var ship_center = _ship.get_current_size() / 2;

    var this_location = Vector2(
        _info["location"][0],
        _info["location"][1]
    );
    
    var relative_location = this_location - ship_center;

    if direction() == 's':
        relative_location.y += engine_center.y;
        
        if engine_size() == 'w':
            relative_location.x += 1;

    return relative_location;

func engine_() -> Engine_:
    return _engine;
