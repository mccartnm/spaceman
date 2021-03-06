extends Node

# -- Imports
const utils               = preload("utils.gd");
const HardpointPrototypes = preload("prototype/hardpoint_proto.gd");
const ShipPrototypes      = preload("prototype/ship_proto.gd");
const EnginePrototypes    = preload("prototype/engine_proto.gd");

# -- Actively Known Assets
onready var HARDPOINTS := HardpointPrototypes.new();
onready var SHIPS      := ShipPrototypes.new();
onready var ENGINES    := EnginePrototypes.new();

func engine_directory() -> String:
    return "res://data/components/engines"
    
func hardpoint_directory() -> String:
    return "res://data/components/hardpoints"
    
func ships_directory() -> String:
    return "res://data/ships"

func projectile_directory() -> String:
    return "res://data/components/bullets"

func _ready():
    """
    The first thing we want to do is bool up the prototypes. This is where
    it happens.
    """
    # -- Hardpoints
    var base_path := hardpoint_directory();
    for filename in utils.list_files_in_directory(base_path, ".si"):
        self.HARDPOINTS.add_prototypes(base_path + "/" + filename);

    # -- Engines
    var engine_path := engine_directory();
    for filename in utils.list_files_in_directory(engine_path, ".si"):
        ENGINES.add_prototypes(engine_path + "/" + filename);

    # -- Ships
    var ship_path := ships_directory();
    for folder in utils.list_files_in_directory(ship_path):
        SHIPS.add_prototype(
            ship_path + "/" + folder,
            HARDPOINTS,
            ENGINES
        );
