extends Node

# Imports
const utils = preload("../utils.gd");
const HardpointPrototypes = preload("hardpoint_proto.gd");
const EnginePrototypes = preload("engine_proto.gd");

var WEIGHT_CLASS: Dictionary = {
    'A' : 1,
    'B' : 2,
    'C' : 3,
    'D' : 4
};

var _ship_prototypes: Dictionary = {};

func new_ship(name: String, position: Vector2):
    """
    Generate a new ship based on the required
    """
    if not _ship_prototypes.has(name):
        return null;

    var ship_scene = load("res://data/ships/{}/{}.tscn".format(
        [name.to_lower(), name.to_lower()], "{}"
    ));
    var s = ship_scene.instance();
    s.boot(_ship_prototypes[name]);
    s.set_position(position);
    return s;

func add_prototype(
    data_directory: String,
    hardpoints:     HardpointPrototypes,
    engines:        EnginePrototypes
):
    """
    Add a ship prototype from a descriptor
    :param data_directory: The directory where the info.si file and all
    required sprites should be located
    :return: null
    """
    var yaml = preload("res://addons/godot-yaml/gdyaml.gdns").new();

    var errors := [];
    var file := File.new();
    var fullpath := data_directory + "/info.si";
    if not file.file_exists(fullpath):
        return false;

    file.open(fullpath, File.READ);
    var info = yaml.parse(file.get_as_text());
    if not (typeof(info) == TYPE_DICTIONARY):
        print ("Ship descriptor must be a dictionary");
        return false;

    var required := [
        ['display_name', TYPE_STRING],
        ['class', TYPE_STRING],
        ['description', TYPE_STRING],
        ['mobile', TYPE_BOOL],
        ['hull', [TYPE_INT, TYPE_REAL]],
        ['shield', [TYPE_INT, TYPE_REAL]],
        ['fuel', [TYPE_INT, TYPE_REAL]],
        ['base_power', [TYPE_INT, TYPE_REAL]]
    ];

    var ok = true
    for d in required:
        if (not utils.must_contain(info, errors, d[0], d[1])):
            ok = false;

    var n: String = info.get('display_name', fullpath);

    if (info.has("hardpoints")):
        if not (typeof(info["hardpoints"]) == TYPE_ARRAY):
            errors.push_back(
                "Hardpoint listing must be an array (Ship: {s})".format({"s":n})
            );
        else:
            for hardpoint_info in info["hardpoints"]:
                var hardpoint_errors := [];
                HardpointPrototypes.verify_ship_hardpoint(
                    hardpoint_info, hardpoint_errors, hardpoints
                );
                if (hardpoint_errors.size() > 0):
                    errors.push_back("Hardpoint Failures: " + n);
                    for e in hardpoint_errors:
                        errors.push_back(e);

    if (info.has("engines")):
        if not (typeof(info["engines"]) == TYPE_ARRAY):
            errors.push_back(
                "Engines listing must be an array (Ship: {s})".format({"s":n})
            );
        else:
            for engine_info in info["engines"]:
                var engine_errors := [];
                EnginePrototypes.verify_ship_engine(
                    engine_info, engine_errors,  engines
                );
                if (engine_errors.size() > 0):
                    errors.push_back("Engine Failures: " + n);
                    for e in engine_errors:
                        errors.push_back(e);

    # At a minimum there must be one sprite of "life/static.png"
    var f := File.new();
    var lifepath: String = data_directory + '/life/static.png';
    if not f.file_exists(lifepath):
        errors.push_back("life/static.png is required for all ships");

    if (errors.size() > 0):
        print ("Error on: {n}".format({"n": n}));
        var joined_string = utils.join(errors, "\n");
        print (joined_string);
        return false;
        
    info["data_directory"] = data_directory;
    _ship_prototypes[n] = info;
