"""
The players station is where we hold onto all kinds of tools
and tech for the user to take advantage of.
"""
extends Node2D

# -- Imports


# -- Members

func from_json(data: Dictionary):
    """
    Using the data provided, build our station
    """
    var base_type = data.get("station_root", "alpha");
    var root_base_component = load(
        "res://scenes/campaign/stations/{}/base.tscn".format(
            [base_type], "{}"
    )).instance();
    
    add_child(root_base_component);
    root_base_component.from_data(base_type, data.get("station_modules", []));

func _ready():
    pass
