extends Node

const utils = preload("../utils.gd");
const Hardpoint = preload("../hardpoint.gd");
const Ship = preload("../ship.gd");

"""
Data class for hardpoints
"""
var BULLET : String  = 'bullet';
var LAZER : String   = 'lazer';
var BOMB : String    = 'bomb';
var MISSILE : String = 'missile';
var MINER : String   = 'miner';
var UTILITY : String = 'utility';
var HARDPONT_TYPES : Array = [
    BULLET, LAZER, BOMB, MISSILE, MINER, UTILITY
];

var _hardpoint_prototypes: Dictionary = {};

static func verify_ship_hardpoint(hardpoint_info: Dictionary, errors: Array, obj):
    """
    Verify that a hardpoint on a ship descriptor is valid
    :param hardpoint_info: The information for our hardpoint
    :param errors: s
    """
    if not typeof(hardpoint_info) == TYPE_DICTIONARY:
        errors.push_back("Hardpoint descriptor should be a dictionary");
        return;

    var required := [
        ['name', TYPE_STRING],
        ['location', TYPE_ARRAY],
        ['direction', [TYPE_INT, TYPE_REAL]],
        ['locked', [TYPE_BOOL]],
        ['command', [TYPE_STRING]],
        ['default', [TYPE_STRING, TYPE_NIL]]
    ];
    
    for d in required:
        utils.must_contain(hardpoint_info, errors, d[0], d[1]);

    if (errors.size() > 0):
        return;

    if not obj._hardpoint_prototypes.has(hardpoint_info["default"]):
        errors.push_back(
                "Unknown hardpoint prototype: {}".format(
                    [hardpoint_info["default"]], "{}"
                )
        );

    var types = hardpoint_info["types"];
    for t in types:
        if not obj.HARDPONT_TYPES.has(t):
            errors.push_back("Invalid type: {}".format([t], "{}"));

    var location = hardpoint_info["location"];
    if location.size() != 2:
        errors.push_back("location must be in [x, y] format")
    else:
        for i in location:
            if not (typeof(i) == TYPE_INT):
                errors.push_back("x, y coordinates should be in ints");

func new_hardpoint(name: String, ship_hp_info: Dictionary, ship: Ship) -> Hardpoint:
    """
    Create a new hardpoint instance to place on a ship
    """
    if not _hardpoint_prototypes.has(name):
        return null;
    return Hardpoint.new(_hardpoint_prototypes[name], ship_hp_info, ship);

func add_prototypes(filename: String):
    """
    Add hardpoint prototypes
    """
    var yaml = preload("res://addons/godot-yaml/gdyaml.gdns").new();
    
    var errors: Array = [];
    var file: File = File.new();
    if not file.file_exists(filename):
        return false

    file.open(filename, File.READ);
    var info = yaml.parse(file.get_as_text());

    if not (typeof(info) == TYPE_ARRAY):
        print ("Hardpoint listing must be an array[dictionary,]");
        return false;

    for hp_info in info:
        if not (typeof(hp_info) == TYPE_DICTIONARY):
            print ("Hardpoint must be a mapping");
            return false;

        var required := [
            ['name', TYPE_STRING],
            ['description', TYPE_STRING],
            ['type', TYPE_STRING],
            ['ammo', [TYPE_STRING, TYPE_NIL]],
            ['damage', [TYPE_INT, TYPE_REAL]],
            ['rate', [TYPE_INT, TYPE_REAL]]
        ];
        
        for d in required:
            utils.must_contain(hp_info, errors, d[0], d[1]);

        var n: String = hp_info.get('name', filename);
        if (errors.size() > 0):
            print ("Error on: {n}".format({"n": n}));
            var joined_string = utils.join(errors, "\n");
            print (joined_string);
            return false;
            
        if _hardpoint_prototypes.has(n):
            print ("Duplicate hardpoint name: {n}".format({"n":n}));
            return false;

        _hardpoint_prototypes[n] = hp_info;