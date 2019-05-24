extends Node2D

var STAR_COUNT = 10000.0;
var MAP_SIZE = Vector2(8000, 8000); # FIXME: Needs to be relative
var _density = 1.0;

#
# We build a collection of stars to render for the user. This makes
# it easy to show a "space-like" vision.
#

func _ready():
    """
    We connect to the resize of the viewport to make sure the stars
    are all around the scene
    """
    get_tree().get_root().connect("size_changed", self, "_build_star_layout");
    set_z_index(-100);
    _build_star_layout();


func _build_star_layout():
    """
    Build a collection of stars
    """
    for child in get_children():
        remove_child(child);

    var total_stars = int(STAR_COUNT * _density);
    var upper_third = int(total_stars / 3);
    var screen = MAP_SIZE;

    var texture = load("res://data/objects/space/star.png");
    for i in range(total_stars):
        var node = Sprite.new();
        if i < upper_third:
            node.scale = node.scale * 0.5 * (randf() * 2 + 1);
        else:
            node.scale = node.scale * 0.3 * (randf() * 2 + 1);
        node.set_name("star_me_" + str(i));
        node.set_texture(texture);
        node.position = Vector2(
            rand_range(-screen.x, screen.x),
            rand_range(-screen.y, screen.y)
        );
        add_child(node);
