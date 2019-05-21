extends Node

const utils = preload("../utils.gd");

var WIDE: String = "w";
var THIN: String = "t";
var CARDINALS: Array = ['n', 's', 'e', 'w'];

var _engine_prototypes: Dictionary = {};

func _ready():
    pass # Nothing be default

static func verify_ship_engine(engine_info: Dictionary, errors: Array, obj):
    """
    Verify that an engine descriptor for a ship is valid
    :param engine_info: The information pertaining to an engine slot on a ship
    :errors: Array of errors that we need populate
    :obj: EnginePrototype instance
    """
    if not typeof(engine_info) == TYPE_DICTIONARY:
        errors.push_back("Engine descriptor should be a dictionary");
        return;

#            ('location', list),
#            ('size', str),
#            ('default', str),
#            ('direction', str),

    var required := [
        ['location', TYPE_ARRAY],
        ['size', TYPE_STRING],
        ['direction', [TYPE_STRING, TYPE_INT, TYPE_REAL]],
        ['default', [TYPE_STRING]],
    ];
    
    for d in required:
        utils.must_contain(engine_info, errors, d[0], d[1]);

    if (errors.size() > 0):
        return;

    var location = engine_info["location"];
    if location.size() != 2:
        errors.push_back("location must be in [x, y] format")
    else:
        for i in location:
            if not (typeof(i) == TYPE_INT):
                errors.push_back("x, y coordinates should be in ints");


    var dir = engine_info['direction'];
    if typeof(dir) == TYPE_STRING and not obj.CARDINALS.has(dir):
        var cards: String = utils.join(obj.CARDINALS, ", ");
        errors.push_back(
            "String direction must be one of: " + cards
        );

    var sizes := [obj.WIDE, obj.THIN];
    if not sizes.has(engine_info['size']):
        errors.append(
            "Engine size must be one of: " + utils.join(sizes, ', ')
        );

func add_prototypes(filename: String):
    """
    Add engine prototypes
    """
    var yaml = preload("res://addons/godot-yaml/gdyaml.gdns").new();

    var errors := [];
    var file := File.new();
    if not file.file_exists(filename):
        return false;

    file.open(filename, File.READ);
    var info = yaml.parse(file.get_as_text());
    if not (typeof(info) == TYPE_ARRAY):
        print ("Engine listing must be an array[dictionary,]");
        return false;

    for eg_info in info:
        if not (typeof(eg_info) == TYPE_DICTIONARY):
            print ("Engine must be a mapping");
            return false;

        var required := [
            ['name', TYPE_STRING],
            ['power', [TYPE_INT, TYPE_REAL]],
            ['sprite', TYPE_STRING],
            ['minimum_class', [TYPE_STRING]]
        ];

        var ok = true
        for d in required:
            if (not utils.must_contain(eg_info, errors, d[0], d[1])):
                ok = false;
                
        var n: String = eg_info.get('name', filename);
        if (errors.size() > 0):
            print ("Error on: {n}".format({"n": n}));
            var joined_string = utils.join(errors, "\n");
            print (joined_string);
            return false;
            
        if _engine_prototypes.has(n):
            print ("Duplicate engine name: {n}".format({"n":n}));
            return false;
            
        # if not ShipPrototypes.new().WEIGHT_CLASS.has(eg_info['minimum_class']):
        #     print ("Unkown engine minimum_class: '{mc}'".format({"mc": eg_info['minimum_class']}));
        #     return false;

        _engine_prototypes[n] = eg_info;