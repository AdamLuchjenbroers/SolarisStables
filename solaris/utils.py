from copy import deepcopy


def get_arg(argument, kwargs, default=None):
    if argument in kwargs:
        return kwargs[argument]
    else:
        return default 

def deepcopy_append(base_list, to_append):
    """ 
    Takes a deepcopy of base_list, and returns it with the items in to_append added
    """   
    new_list = deepcopy(base_list)
        
    for item in to_append:
        new_list.append(item)
        
    return new_list

def determine_selected(request):
    # Dirty hack to supply wiki functionality 
    if request.path[0:5] == '/wiki':
        return {'selected' : 'Wiki'}
    else:
        return {}
    