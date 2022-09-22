'''Info Header Start
Name : fade
Author : Alpha Moonbase
Version : 0
Build : 13
Savetimestamp : 1663850219
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import tween_value
import td, math
from dataclasses import dataclass



@dataclass
class tween:
	parameter		:	td.Par
	time			:   float
	start_value		:	tween_value.tween_value
	target_value	:   tween_value.tween_value
	interpolation	:	str = "LinearInterpolation"
	current_step	:	float 	= 0

	def increment_step(self, stepsize):
		stepsize = stepsize or absTime.stepSeconds
		self.current_step += stepsize
		#self.current_step = tdu.clamp( self.current_step + stepsize, 0, self.time )

	@property
	def done(self):
		return self.current_step >= self.time

	def Delay(self, offset):
		self.current_step -= abs(offset)

	def Step(self, stepsize = None):
		pass
		
	def Finish(self):
		pass
		
class fade( tween ):

	def Step(self, stepsize = None):
		self.increment_step(stepsize)
		curves = op("curves_repo").Repo
		curve_value = curves.GetValue( self.current_step, self.time, self.interpolation )
		start_evaluated = self.start_value.eval()
		target_evaluated = self.target_value.eval()
		difference = target_evaluated - start_evaluated
		new_value = start_evaluated + difference * curve_value
		self.parameter.val = new_value
		if self.done: self.Finish()

	def Finish(self):
		self.target_value.assign_to_par( self.parameter )

class endsnap( tween ):

	def Step(self, stepsize = None):
		self.increment_step(stepsize)
		if self.done: self.Finish

	def Finish(self):
		self.target_value.assign_to_par( self.parameter )

class startsnap( tween ):

	def Step(self, stepsize = None):
		self.target_value.assign_to_par( self.parameter )
		self.increment_step(stepsize)

