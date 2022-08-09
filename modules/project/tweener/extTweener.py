'''Info Header Start
Name : extTweener
Author : Alpha Moonbase
Version : 0
Build : 10
Savetimestamp : 1660063257
Saveorigin : Project.toe
Saveversion : 2021.16410
Info Header End'''

import fade
import tween_value

_type = type

class extTweener:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 	= ownerComp
		self.fades:dict 	= {}
	
		self.Exceptions = mod.tweener_exceptions
								
		self.delay_script 	= "me.CreateTween( args[0], args[1], args[2], type = args[3], curve = args[4], id = args[5], mode = args[6], expression = args[7], delay = 0)"
		self.callback 		= self.ownerComp.op('callbackManager')

	def getFadeId(self, par):
		return hash(par)

	def FadeStep(self, step_in_ms = None):
		fadesCopy = self.fades.copy()
		for fade_id, tween_object in fadesCopy.items():
			tween_object.Step(step_in_ms)
			if tween_object.done: del self.fades[ fade_id ]
		

	def AbsoluteTweens(self, list_of_tweens, curve = "s", time=1):
		for tween in list_of_tweens:
			self.AbsoluteTween(
				tween["par"],
				tween["end"],
				tween.get("time", time),
				curve = tween.get("curve", curve),
				delay = tween.get("delay", 0)
			)

	def RelativeTweens(self, list_of_tweens, curve = "s", time=1):
		for tween in list_of_tweens:
			self.RelativeTween(
				tween["par"],
				tween["end"],
				tween.get("time", time),
				curve = tween.get("curve", curve),
				delay = tween.get("delay", 0)
			)
	
	def AbsoluteTween(self, par, end, time, curve = 's', delay = 0):
		self.CreateTween(par, end, time, curve = curve, delay = delay)
		return

	def RelativeTween(self, par, end, speed, curve = 's', delay = 0):
		difference = abs(end - par.eval())
		time = difference / speed
		self.CreateTween(par, end, time, curve = curve, delay = delay)
		return
	
	def CreateTween(self,parameter, end:float, time:float, type:str = 'fade', curve:str = 's', id = '', mode = 'CONSTANT', expression = None, delay = 0):
		if not isinstance( parameter, Par):
			raise self.Exceptions.TargetIsNotParameter(f"Invalid Parameterobject {parameter}")
		
		target_value 	= tween_value.tween_value_from_arguments( parameter, mode, expression, end )
		start_value 	= tween_value.tween_value_from_parameter( parameter )

		fade_class:fade.tween  	= getattr( fade, type, fade.startsnap )
		debug("Creating fade for parameter", parameter)
		debug("Got fade_class", fade_class)
		fade_object = fade_class( parameter, time, start_value, target_value, interpolation = curve) 
		fade_object.Delay( delay )
		self.fades[self.getFadeId( parameter )] = fade_object
		

	def StopFade(self,par):
		del self.fades[self.getFadeId(par)]

	def StopAllFades(self):
		self.fades = {}

	def ClearFades(self):
		self.fades.clear()

	def PrintFades(self):
		print(self.fades)