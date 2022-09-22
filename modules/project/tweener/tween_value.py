'''Info Header Start
Name : tween_value
Author : Alpha Moonbase
Version : 0
Build : 12
Savetimestamp : 1663849707
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import td
from functools import lru_cache
import tweener_exceptions
from typing import Union

class tween_value:
    def eval(self):
        pass

    def assign_to_par(self, parameter):
        pass

class expression_value( tween_value ):
    def __init__(self, parameter, expression_string):
        self.expression_string = expression_string
        self.expression_function = lambda : parameter.owner.evalExpression( expression_string )
    
    def eval(self):
        return self.expression_function()

    def assign_to_par(self, parameter):
        parameter.mode = ParMode.EXPRESSION
        parameter.expr = self.expression_string
        

class static_value( tween_value ):
    def __init__(self, parameter, value):
        self.value = type( parameter.val)(value)

    def eval(self):
        return self.value

    def assign_to_par(self, parameter):
        parameter.val = self.eval()

par_modes = [parmode.name.upper() for parmode in ParMode._value2member_map_.values()]

@lru_cache(None)
def stringify_parmode( mode ):
    if isinstance(mode, ParMode): return mode.name.upper()
    if isinstance(mode, str) and mode.upper() in par_modes: return mode.upper()
    raise tweener_exceptions.InvalidParMode

def tween_value_from_parameter( parameter:td.Par ):
    if parameter.mode.name =="EXPRESSION": return expression_value( parameter, parameter.expr )
    return static_value( parameter, parameter.eval() )

def tween_value_from_arguments( parameter:td.Par, mode:Union[str, ParMode], expression:str, value:any):
    if stringify_parmode(mode) =="EXPRESSION" and expression: return expression_value( parameter, expression )
    return static_value( parameter, value )

