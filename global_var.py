def _init():
    global _global_dict
    _global_dict = {}

def set_value(key,value):
    _global_dict[key] = value

def update_value(key,value):
    _global_dict[key] = value

def get_value(key):
    try:
        return _global_dict[key]
    except  Exception as result:
        print(result.__traceback__.tb_frame.f_globals['__file__'])
        print(result.__traceback__.tb_lineno)
        print(repr(result))

def value_exist(key):
    return key in _global_dict