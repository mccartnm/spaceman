"""
Stargates hold the key to traversing our world. This is how we go from
peaceful settlements to hostile realms filled with loot and dissaster!
"""

extends StaticBody2D

# -- Signals
signal stargate_activated(stargate, ship);

# -- Imports
const TSprite = preload("../tsprite.gd");

# -- Members
var _sprite: TSprite;

func boot(gate: String):
    _sprite = TSprite.new(
        "res://data/stargate/{}".format([gate], "{}"),
        TSprite.AnimationLoadType.Stargate
    );
    add_child(_sprite);
    _sprite.play("life-static");

    $CouldAnimation.play("clouds");
    $RunwayAnimation.play("runway_bob");

    # For a dark portal
#    _sprite.modulate = Color(1, 0, 0);
#    $SpaceCould.modulate = Color(1, 0.5, 0.5);


func ship_collision(ship):
    """
    In the event a ship collides with our startgate - we send them
    away!
    """
    emit_signal("stargate_activated", self, ship);

    # Until we learn more from our player - let's set the ship
    # in a stable state and go from there
    $CollisionShape2D.disabled = true;
    if ship.player():
        ship.player().set_can_control(false);

    ship.set_thrust(Vector2(0,0));
    ship.set_speed(Vector2(0,0));


func activate_warp(ship):
    """
    We start the warp process
    """
    pass


func _ready():
    pass