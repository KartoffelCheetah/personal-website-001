#!.venv/bin/python3
#-*- coding:utf-8 -*-
from console_paint import painter

def painterColor(color) :
    def wrap(func) :
        def new_function(*args, **kwargs) :
            painter(*args, color=color, **kwargs)
        return new_function
    return wrap

@painterColor('#888844')
def printWarning(*args, **kwargs) :
    pass
@painterColor('#ee6644')
def printAlert(*args, **kwargs) :
    pass
@painterColor('#33dd55')
def printOK(*args, **kwargs) :
    pass
