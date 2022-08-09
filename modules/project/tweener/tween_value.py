'''Info Header Start
Name : tween_value
Author : Alpha Moonbase
Version : 0
Build : 7
Savetimestamp : 1660057980
Saveorigin : Project.toe
Saveversion : 2021.16410
Info Header End'''

import td
class tween_value:
    def eval(self):
        pass

    def assign_to_par(self, parameter):
        pass

class expression_value( tween_value ):
    def __init__(self, parameter, expression_string):
        self.expression_function = lambda : parameter.owner.evalExpression( expression_string )
    
    def eval(self):
        return self.expression_function()

    def assign_to_par(self, parameter):
        parameter.mode = "EXPRESSION"
        parameter.expr = self.expression_string
        

class static_value( tween_value ):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def assign_to_par(self, parameter):
        parameter.val = self.eval()

def tween_value_from_parameter( parameter:td.Par ):
    if parameter.mode.name =="EXPRESSION": return expression_value( parameter, parameter.expr )
    return static_value( parameter.eval() )

def tween_value_from_arguments( parameter:td.Par, mode:str, expression:str, value:any):
    if mode.upper() =="EXPRESSION" and expression: return expression_value( parameter, expression )
    return static_value( value )

