'''Info Header Start
Name : fade
Author : Alpha Moonbase
Version : 0
Build : 7
Savetimestamp : 1659986744
Saveorigin : Project.toe
Saveversion : 2021.16410
Info Header End'''
import tween_value
import td


curves = op("curves")

class tween:
	current_step 	= 0
	time 			= 0
	def __init__(self, 	parameter:td.Par, 
						time:float, 
						start_value:tween_value.tween_value, 
						target_value:tween_value.tween_value, 
						interpolation:str = "LinearInterpolation"):
		pass

	def increment_step(self, stepsize):
		stepsize = stepsize or absTime.stepSeconds * 1000
		self.current_step = tdu.clamp( self.current_step + stepsize, 0, self.time )

	@property
	def done(self):
		return self.current_step >= self.time

	def Step(self, stepsize = None):
		return
		
	def Finish(self):
		return
		
class fade( tween ):
	def __init__(self, 	parameter:td.Par, 
						time:float, 
						start_value:tween_value.tween_value, 
						target_value:tween_value.tween_value, 
						interpolation:str = "LinearInterpolation"):
		self.time 			= time * 1000
		self.parameter 		= parameter
		self.start_value 	= start_value
		self.target_value 	= target_value
		self.interpolation 	= interpolation

	def Step(self, stepsize = None):
		self.increment_step(stepsize)
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
	def __init__(self, 	parameter:td.Par, 
						time:float, 
						start_value:tween_value.tween_value, 
						target_value:tween_value.tween_value, 
						interpolation:str = "LinearInterpolation"):
		self.parameter = parameter
		self.time = time
		self.target_value = target_value

	def Step(self, stepsize = None):
		self.increment_step(stepsize)
		if self.done: self.Finish

	def Finish(self):
		self.target_value.assign_to_par( self.parameter )

class startsnap( tween ):
	def __init__(self, 	parameter:td.Par, 
						time:float, 
						start_value:tween_value.tween_value, 
						target_value:tween_value.tween_value, 
						interpolation:str = "LinearInterpolation"):
		self.parameter = parameter
		self.time = time
		self.target_value = target_value

	def Step(self, stepsize = None):
		self.target_value.assign_to_par( self.parameter )
		self.increment_step(stepsize)

