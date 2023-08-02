
'''Info Header Start
Name : extTweener
Author : Alpha Moonbase
Version : 0
Build : 12
Savetimestamp : 1663849167
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''

import fade
import tween_value

from typing import Union, Hashable


_type = type

class extTweener:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 	= ownerComp
		self.Tweens:dict 	= {}
	
		self.Exceptions = mod.tweener_exceptions
								
		self.callback 		= self.ownerComp.op('callbackManager')

	def getFadeId(self, par):
		return hash(par)

	def FadeStep(self, step_in_ms = None):
		fadesCopy = self.Tweens.copy()
		for fade_id, tween_object in fadesCopy.items():
			tween_object.Step(step_in_ms)
			if tween_object.done: del self.Tweens[ fade_id ]
		

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
	
	def CreateTween(self,parameter, 
					end:float, 
					time:float, 
					type:str 					= 'fade', 
					curve:str 					= 's', 
					id:Hashable 				= '', 
					mode:Union[str, ParMode] 	= 'CONSTANT', 
					expression:str 				= None, 
					delay:float 				= 0.0):
		if not isinstance( parameter, Par):
			raise self.Exceptions.TargetIsNotParameter(f"Invalid Parameterobject {parameter}")
		
		target_value 	= tween_value.tween_value_from_arguments( parameter, mode, expression, end )
		start_value 	= tween_value.tween_value_from_parameter( parameter )

		fade_class:fade.tween  	= getattr( fade, type, fade.startsnap )
		fade_object 			= fade_class( parameter, time, start_value, target_value, interpolation = curve) 
		fade_object.Delay( delay )
		self.Tweens[id or self.getFadeId( parameter )] = fade_object
		

	def StopFade(self,par):
		del self.Tweens[self.getFadeId(par)]

	def StopAllFades(self):
		self.Tweens = {}

	def ClearFades(self):
		self.Tweens.clear()

	def PrintFades(self):
		print(self.Tweens)