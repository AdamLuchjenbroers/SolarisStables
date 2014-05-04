import re

def expect_integer(function):
    def check(*args, **kwargs):
        value = function(*args, **kwargs)
        try:
            return int(value)
        except ValueError:
            return None
    
    return check

def expect_regex(function, regex):
    r_compiled = re.compile(regex)
    
    def check(*args, **kwargs):
        value = function(*args, **kwargs)
        if r_compiled.match(value):
            return value
        else:
            return None
    
    return check  
    
def expect_alphastring(function):
    return expect_regex(function, '^[a-zA-Z ]+$')
    
def expect_basicstring(function):
    return expect_regex(function, '^[a-zA-Z0-9 \(\)\-\']+$')