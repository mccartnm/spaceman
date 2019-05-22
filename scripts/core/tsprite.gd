"""
Sprite(s) that can manage multiple states
"""
extends AnimatedSprite

signal anim_state_changed;

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
var _current_state: String = 'life-static';
var _anim_regex: RegEx;

# -- Public Interface

func set_animation_state(state: String) -> bool:
    """
    Set the current animation state
    :param state: The new state to use. If the state does
    not exist, the state is set to 'life-static' and we return
    false
    :return: true if the state change was available 
    """
    if _states.has_animation(state):
        _current_state = state;
        emit_signal("anim_state_changed");
        return true;
    return false;

func get_current_size() -> Vector2:
    """
    :return: The current size of this sprite
    """
    var tex: Texture = _states.get_frame(_current_state, get_frame());
    if tex:
        return tex.get_size() * get_scale();
    return Vector2(0, 0);

# -- Private Interface

func _init(data_directory: String, load_type, name: String = ""):
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
            _load_component_sprites(data_directory, name);
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


func _load_component_sprites(data_path: String, name: String):
    """
    Loading, what is most likely a simple setup, for
    basic sprite utilities
    """
    var f = File.new();
    
    var textures := [];
    var single = data_path + '/' + name + '.png';
    if f.file_exists(single):
        textures.push_back(load(single));
        
    else:
        var dir = Directory.new();
        var dpath = data_path + '/' + name
        if dir.dir_exists(dpath):
            var regex = RegEx.new();
            regex.compile('^' + name + "_\\d+\\.png$");
            for filename in utils.list_files_in_directory(dpath):
                if regex.search(filename):
                    textures.push_back(load(
                        utils.join([data_path, name, filename], '/')
                    ));

    _states.add_animation("life-static");
    for t in textures:
        _states.add_frame("life-static", t);
