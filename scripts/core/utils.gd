extends Node

"""
Collection of static functions and utilities
"""

func _ready():
    pass

static func join(array: Array, string: String) -> String:
    return PoolStringArray(array).join(string);

static func must_contain(info: Dictionary, errors: Array, key: String, is_type) -> bool:
    """
    Match containment
    """
    if not info.has(key):
        errors.push_back("Missing key: '{0}'".format({"0":key}));
        return false

    var ok = false;
    if (typeof(is_type) == TYPE_ARRAY):
        for t in is_type:
            if (typeof(info[key]) == t):
                ok = true;
        if not ok:
            errors.push_back("'{0}' wrong type!".format({"0":key}));
            return false;
        return true;

    if (typeof(info[key]) != is_type):
        errors.push_back("'{0}' wrong type!".format({"0":key}));
        return false;
    return true;

static func list_files_in_directory(path: String, extension: String = "") -> Array:
    """
    Pretty straight forward
    """
    var files := [];
    var dir := Directory.new();
    if dir.open(path):
        return files;
    if dir.list_dir_begin():
        return files;

    while true:
        var file: String = dir.get_next();
        if file == "":
            break;
        elif file.begins_with("."):
            continue;
        if extension != "":
            if not file.ends_with(extension):
                continue;
        files.push_back(file);
    return files;