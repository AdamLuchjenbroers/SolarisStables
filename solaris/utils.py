
def get_arg(argument, kwargs, default=None):
    if argument in kwargs:
        return kwargs[argument]
    else:
        return default 
