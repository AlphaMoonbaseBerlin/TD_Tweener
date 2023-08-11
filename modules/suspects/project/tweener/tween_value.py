
'''Info Header Start
Name : tween_value
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 13
Savetimestamp : 2023-08-11T18:01:26.587417
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import td
from functools import lru_cache
import tweener_exceptions
from typing import Union

par_modes = [parmode.name.upper() for parmode in ParMode._value2member_map_.values()]

class _tweenValue:
    def eval(self):
        pass

    def assignToPar(self, parameter):
        pass

class expressionValue( _tweenValue ):
    def __init__(self, parameter, expression_string):
        self.expressionString = expression_string
        self.expressionFunction = lambda : parameter.owner.evalExpression( expression_string )
    
    def eval(self):
        return self.expressionFunction()

    def assignToPar(self, parameter):
        parameter.mode = ParMode.EXPRESSION
        parameter.expr = self.expressionString
        

class staticValue( _tweenValue ):
    def __init__(self, parameter, value):
        self.value = type( parameter.val)(value)

    def eval(self):
        return self.value

    def assignToPar(self, parameter):
        parameter.val = self.eval()



@lru_cache(None)
def stringifyParmode( mode ):
    if isinstance(mode, ParMode): return mode.name.upper()
    if isinstance(mode, str) and mode.upper() in par_modes: return mode.upper()
    raise tweener_exceptions.InvalidParMode

def tweenValueFromParameter( parameter:td.Par ):
    if parameter.mode.name =="EXPRESSION": return expressionValue( parameter, parameter.expr )
    return staticValue( parameter, parameter.eval() )

def tweenValueFromArguments( parameter:td.Par, mode:Union[str, ParMode], expression:str, value:any):
    if stringifyParmode(mode) =="EXPRESSION" and expression: return expressionValue( parameter, expression )
    return staticValue( parameter, value )
    

