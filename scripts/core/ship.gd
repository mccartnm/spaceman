extends KinematicBody2D

# -- Signals
signal ship_health_changed;
signal ship_hardpoints_changed;
signal ship_engines_changed;
signal ship_location_changed;

# -- Imports
const ShipHardpoint = preload("components/ship_hardpoint.gd");
const ShipEngine    = preload("components/ship_engine.gd");

const Hardpoint = preload("hardpoint.gd");
const Engine_   = preload("engines.gd");
const TSprite   = preload("tsprite.gd");

# -- Members
var _info: Dictionary;
var _hardpoints: Array;
var _engines: Array;
var _data_location: String;
var _sprite: TSprite;

# Movement
var _thrust: Vector2;
var _speed: Vector2;
var _drag: Vector2 = Vector2(0.8, 0.8);
var _angle_delta: float;

# Visibility
var _camera: Camera2D;
var _active: bool = false;

# Health
var _hull: float;
var _shield: float;
var _max_hull: float;
var _max_shield: float;

# -- Public Methods

func set_thrust(thrust: Vector2):
    _thrust = thrust;
    for engine in _engines:
        engine.check_state(_thrust);


func get_current_size() -> Vector2:
    return Vector2(64, 64);


func set_angle_delta(angle_delta: float):
    _angle_delta = angle_delta;


func fire_command(command: String) -> void:
    for sh in _hardpoints:
        var hp = sh.hardpoint();
        if not hp:
            continue
        
        if sh.command() == command:
            hp.fire();

func release_command(command: String) -> void:
    for sh in _hardpoints:
        var hp = sh.hardpoint();
        if not hp:
            continue

        if sh.command() == command:
            hp.release();

func max_speed() -> float:
    """
    Based on the weight class and the current engine loadout, we get
    the maximum speed that can be achieved.
    """
    var total_power = 0.0;
    for engine in _engines:
        total_power += engine.power();
    return total_power / PrototypeLoader.SHIPS.WEIGHT_CLASS[class_()];

func class_() -> String:
    return _info['class'];

func follow():
    """
    Enable a camera on this ship and follow them about!
    
    Typically this is used for the player but could also proove useful
    for cutscenes and things like that
    """
    if not _camera:
        _camera = Camera2D.new();
        add_child(_camera);
    
    _camera.current = true;
    _camera.smoothing_enabled = true;
    _camera.smoothing_speed = 5;
    _active = true;

# -- Private Methods

func _init(ship_info: Dictionary):
    """
    Construct a ship!
    """
    _info = ship_info;
    _engines = [];
    _hardpoints = [];
    
    _speed = Vector2(0, 0);
    _thrust = Vector2(0, 0);
    _angle_delta = 0;
    
    _hull = _info['hull'];
    _max_hull = _info['hull'];

    _shield = _info['shield'];
    _max_shield = _info['shield'];

    for hp_info in _info["hardpoints"]:
        _hardpoints.push_back(ShipHardpoint.new(hp_info, self));
    for eg_info in _info["engines"]:
        _engines.push_back(ShipEngine.new(eg_info, self));

    _data_location = _info['data_directory'];
    _sprite = TSprite.new(_data_location, TSprite.AnimationLoadType.Ship);


func _drag_calculation(vec: Vector2) -> Vector2:
    """
    Drag calculation for the ship thrust
    """
    if vec.x > 0:
        vec.x = max(vec.x - _drag.x, 0.0);
    if vec.y > 0:
        vec.y = max(vec.y - _drag.y, 0.0);

    if vec.x < 0:
        vec.x = min(vec.x + _drag.x, 0.0);
    if vec.y < 0:
        vec.y = min(vec.y + _drag.y, 0.0);
    return vec;


func _physics_process(delta):
    """
    Every tick, make sure we're in the right location
    """
    _speed = _drag_calculation(_speed);
    _speed += _thrust    * 10; # Weird constants...
    var ms = max_speed() * 50;
    _speed.x = clamp(_speed.x, -ms, ms);
    _speed.y = clamp(_speed.y, -ms, ms);

    var rad_angle = deg2rad(_angle_delta);
    var new_angle = get_rotation() + rad_angle;
    set_rotation(new_angle);

    var current_pos = global_position;

    var change = _speed * 50;
    change = change.rotated(new_angle);
    move_and_slide(change * delta);

    if _active and global_position != current_pos:
        emit_signal("ship_location_changed");

func _ready():
    add_child(_sprite);
