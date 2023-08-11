
'''Info Header Start
Name : fade
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 15
Savetimestamp : 2023-08-11T18:01:25.750912
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import tween_value
import td
from dataclasses import dataclass, field


import typing

@dataclass
class _tween:
	parameter		:	td.Par
	time			:   float
	startValue		:	tween_value._tweenValue
	targetValue		:   tween_value._tweenValue
	interpolation	:	str 			= "LinearInterpolation"
	_currentStep	:	float 			= field( default= 0, repr=False)
	_callback		: 	typing.Callable = field( default = lambda value: None, repr=False)

	def _incrementStep(self, stepsize):
		stepsize = stepsize or absTime.stepSeconds
		self._currentStep += stepsize
		#self.current_step = tdu.clamp( self.current_step + stepsize, 0, self.time )

	@property
	def done(self):
		return self._currentStep >= self.time

	def Delay(self, offset):
		self._currentStep -= abs(offset)

	def Step(self, stepsize = None):
		pass
		
	def Finish(self):
		pass
		
class fade( _tween ):
	def Step(self, stepsize = None):
		self._incrementStep(stepsize)
		curves 				= op("curves_repo").Repo
		curve_value 		= curves.GetValue( self._currentStep, self.time, self.interpolation )
		start_evaluated 	= self.startValue.eval()
		target_evaluated 	= self.targetValue.eval()
		difference 			= target_evaluated - start_evaluated
		new_value 			= start_evaluated + difference * curve_value
		self.parameter.val = new_value
		if self.done: self.Finish()

	def Finish(self):
		self.targetValue.assignToPar( self.parameter )
		self._callback( self )

class endsnap( _tween ):

	def Step(self, stepsize = None):
		self._incrementStep(stepsize)
		if self.done: self.Finish

	def Finish(self):
		self.targetValue.assignToPar( self.parameter )
		self._callback( self )

class startsnap( _tween ):

	def Step(self, stepsize = None):
		self.targetValue.assignToPar( self.parameter )
		self._incrementStep(stepsize)

