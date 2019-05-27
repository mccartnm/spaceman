class_name StationComponent

extends StaticBody2D

export(float) var _energy;
export(float) var _life_support;

export(bool) var _general;

func from_data(base_name: String, data: Array):
    """
    :param data: Array[Dictionary] that describe this stations
    current state.

    # Example
    [{
        'name' : 'energy_module_small',
        'general' : true,
        #                  this         module
        'connection' : ['mount_t_0', 'mount_b_0'],
        ''
    }]
    """
    for d in data:
        var component;
        var component_path = "res://scenes/campaign/stations"
        if d.get('general', false):
            component_path = component_path + '/general'
        else:
            component_path = component_path + '/' + base_name;

        component_path += '/{}.tscn'.format([d['name']], '{}')
        component = load(component_path).instance();
        
        add_child(component);
        
        # Get the location of this node:
        var conn = d['connection'];
        var connection_node = get_node('mounts/{}'.format(
            [conn[0]], '{}'
        ));
        component.connect_with_station(connection_node.position, conn[1]);
        component.from_data(base_name, d.get('modules', [])); # Rinse repeat

func connect_with_station(pos: Vector2, conn_name: String):
    """
    Move our mount point to the parent. This is a relative operation!
    :param pos: The position of our parent we'll be moving to.
    :param conn_name: The connection this component has in it's mounts/
    list
    """
    var loc = get_node('mounts/{}'.format([conn_name], '{}')).position;
    position = pos - loc;

func _ready():
    pass
