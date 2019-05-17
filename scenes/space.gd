extends Node2D

var STAR_COUNT = 200.0;
var star_node = null;
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
    star_node = Node2D.new();
    add_child(star_node);
    _build_star_layout();

func _build_star_layout():
    """
    Build a collection of stars
    """
    for child in star_node.get_children():
        star_node.remove_child(child);

    var total_stars = int(STAR_COUNT * _density);
    var upper_third = int(total_stars / 3);
    var viewport = get_viewport();
    var screen = Vector2(viewport.size.x, viewport.size.y);
    
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
            rand_range(0, screen.x),
            rand_range(0, screen.y)
        );
        star_node.add_child(node);
