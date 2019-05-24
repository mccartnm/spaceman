extends KinematicBody2D

# -- Import
const TSprite = preload("../tsprite.gd");

# -- Members
var _damage;
var _range;
var _owner;
var _sprite: TSprite;

var _speed;
var _velocity: Vector2;
var _traveled: float = 0.0;

var _audio_player: AudioStreamPlayer2D;

func start(
    name: String, damage, origin: Vector2, range_, owning_obj
):
    _sprite = TSprite.new(
        PrototypeLoader.projectile_directory(),
        TSprite.AnimationLoadType.Component,
        name
    );
    add_child(_sprite);

    set_z_index(owning_obj.get_z_index() - 1);

    set_rotation(owning_obj.global_rotation);
    set_position(origin);

    _owner = owning_obj;
    _range = range_;
    _damage = damage;

    _speed = 750; # FIXME
    _velocity = Vector2(0, -_speed).rotated(rotation);
    _traveled = 0;

    # Give ourselves a little sound
    _audio_player = get_node("AudioStreamPlayer2D");
    _audio_player.play(0.1); # ??

func _physics_process(delta):
    """
    Update our position based
    """
    _traveled += _speed;
    if (_traveled > _range * 40):
        queue_free();
        return;

    var collision = move_and_collide(_velocity * delta);
    if collision:
        _velocity = _velocity.bounce(collision.normal)
        if collision.collider.has_method("hit"):
            collision.collider.hit(_damage)

        # -- Currently, anything we collide with, we're going
        # to destroy outselves on
        queue_free();

func _on_VisibilityNotifier2D_screen_exited():
    queue_free()

func _ready():
    pass
