
_settings = {}

def set_setting(key, value):
    _settings[key] = value

def get_setting(key, default=None):
    return _settings.get(key, default)