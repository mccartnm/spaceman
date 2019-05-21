"""
Sprite(s) that can manage multiple states
"""
extends AnimatedSprite

# -- Imports
const utils = preload("utils.gd");

# -- Enums
enum AnimationLoadType {
    Ship,
    Component,
    Custom
};

# -- Members
var _states: SpriteFrames;
var _anim_regex: RegEx;

# -- Public Interface

# -- Private Interface

func _init(data_directory: String, load_type):
    """
    Construct a sprite based on data layout
    """
    _states = SpriteFrames.new();
    _anim_regex = RegEx.new();
    _anim_regex.compile("^(?P<name>.+)_(?P<frame>\\d+)\\.png$");
    
    match load_type:
        AnimationLoadType.Ship:
            _load_ship_sprites(data_directory);
        AnimationLoadType.Component:
            _load_component_sprites(data_directory);
        AnimationLoadType.Custom:
            pass
    set_sprite_frames(_states);
    set_animation("life-static");

func _load_ship_sprites(data_directory: String):
    """
    Load sprite states based on the directory structure for a ship
    """
    var dir = Directory.new();
    if dir.open(data_directory):
        return

    for filename in utils.list_files_in_directory(data_directory):
        if not dir.dir_exists(filename):
            continue # Must be a directory

        var textures := utils.list_files_in_directory(
            data_directory + "/" + filename, ".png"
        )
        textures.sort();

        var animations := {};
        for texture in textures:
            #
            # For each of the textures found, attmept to build out any
            # animation states that may be present
            #
            var anim_match = _anim_regex.search(texture);
            var name: String;
            if anim_match:
                name = anim_match.get_string("name");
            else:
                name = texture.left(texture.length() - 4); # no .png

            var state := utils.join([filename, name], "-");
            if not _states.has_animation(state):
                _states.add_animation(state);
            
            var full_path = utils.join([data_directory, filename, texture], "/");
            _states.add_frame(state, load(full_path));


func _load_component_sprites(data_directory: String):
    pass