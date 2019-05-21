"""
A/The player! This holds onto the state of our current user
"""
extends Node

# -- Imports
const Ship = preload("ship.gd");
const PlayerInventory = preload("inventory.gd");

# -- Signals
signal ship_changed;
signal ship_took_damage;

# -- Variables
var _ship: Ship = null;
var _can_control: bool = true;

# -- Ready vars
onready var _inventory := PlayerInventory.new();

# -- Public methods

func ship() -> Ship:
    return _ship;
    
func set_ship(ship: Ship):
    _ship = ship;
    emit_signal("ship_changed");

# -- Private Methods

func _ready():
    pass

func _process(delta):
    """
    User input will flow through here
    """
    pass
    
func _physics_process(delta):
    if not _ship or not _can_control:
        return;

    var angle_delta: float = 0.0;
    var velocity = Vector2()  # The player's movement vector.

    if Input.is_action_pressed("ui_strafe_right"):
        velocity.x += 1

    if Input.is_action_pressed("ui_strafe_left"):
        velocity.x -= 1

    if Input.is_action_pressed("ui_down"):
        velocity.y += 1

    if Input.is_action_pressed("ui_up"):
        velocity.y -= 1
 
    if Input.is_action_pressed("ui_left"):
        angle_delta = -3;

    if Input.is_action_pressed("ui_right"):
        angle_delta = 3;

    _ship.set_thrust(velocity.normalized());
    _ship.set_angle_delta(angle_delta);
