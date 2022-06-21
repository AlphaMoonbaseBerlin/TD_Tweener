'''Info Header Start
Name : extTweener
Author : Admin
Version : 0
Build : 4
Savetimestamp : 1655840542
Saveorigin : Project.toe
Saveversion : 2021.16410
Info Header End'''


class extTweener:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 	= ownerComp
		self.fades 		= {}
		self.Types 		= ['fade', 'endsnap', 'startsnap'] 
		
		self.Exceptions = mod.tweener_exceptions
	
		self.Curves 	= self.ownerComp.op('curves') 
		self.finished_fades = {} 
		self.par_modes 		= {
			"BIND"			: "BIND",
			"EXPORT"		: "CONSTANT",
			"EXPRESSION" 	: "EXPRESSION",
			"CONSTANT"		: "CONSTANT", }
			
			
		self.Actions = { 	'fade'		:	self.CreateFade,
							'endsnap'	:	self.CreateEndSnap,
							'startsnap'	:	self.CreateStartSnap,
							}
							
		self.delay_script 	= "me.CreateTween( args[0], args[1], args[2], type = args[3], curve = args[4], id = args[5], mode = args[6], expression = args[7], delay = 0)"
		self.callback 		= self.ownerComp.op('callbackManager')

	def getFadeId(self, par):
		return hash(par)

	def FadeStep(self, step_in_ms = None):
		fadesCopy = self.fades.copy()
		
		timestep = step_in_ms or absTime.stepSeconds * 1000

		for current_fade_id in fadesCopy:
			fade_finished = False
			fade = self.fades[current_fade_id]

			if not fade["par"].valid:
				del self.fades[current_fade_id]
				continue

			fade['stepsTaken'] += timestep
			
			if fade['stepsTaken'] >= fade['timems']:
				fade['stepsTaken'] = fade['timems']
				fade_finished = True
			
			if fade['type'] == 'fade' :
				if fade['mode'] == 'EXPRESSION': 
					
					fade['end'] = fade['par'].owner.evalExpression(fade['expression'])

				position = self.Curves.GetValue(fade['stepsTaken'], fade['timems'], fade['curve'])
				newValue = tdu.remap(position, 0, 1, fade['start'], fade['end'])
				fade['par'].val = newValue
					
			if fade_finished:
				
				fade['par'].mode = ParMode[fade['mode']]
				if fade['mode'] == 'EXPRESSION': fade['par'].expr = fade['expression']
				
				self.finished_fades[fade['preset_id']] = True
				del self.fades[current_fade_id]
				
		for finished_fade in self.finished_fades:
			self.callback.Execute("OnFadeEnd")(finished_fade)
			
		self.finished_fades.clear()

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
	
	def CreateTween(self,par, end:float, time:float, type:str = 'fade', curve:str = 's', id = '', mode = 'CONSTANT', expression = None, delay = 0):
		if not isinstance( par, Par):
			raise self.Exceptions.TargetIsNotParameter(f"Invalid Parameterobject {par}")
		if delay:
			run( self.delay_script, par, end, time, type, curve, id, mode, expression, fromOP = self.ownerComp, delayMilliSeconds = delay * 1000 )
			return 
		if time > 0 : 
			self.Actions[type](par, end, time, type, curve, id, mode, expression)
			return
		
		self.CreateStartSnap(par, end, time, type, curve, id, mode, expression)
		return
	
	def CreateFade(self,par, end:float, time:float, type:str = 'fade', curve:str = 'lin', id = '', mode = 'CONSTANT', expression = None):
	
		mode = self.par_modes[mode]
		
		if par.expr == expression and par.mode == ParMode['EXPRESSION']: return
		if par.eval() != end:
			self.fades[self.getFadeId(par)] ={
				'par'			:	par,
				'end'			:	end,
				'start' 		:	par.eval(),
				'stepsTaken'	:	0.0,
				'timems'		:	time * 1000,
				'type'			:	type,
				'curve'			:	curve,
				'preset_id'		:	id,
				'mode'			:	mode,
				'expression'	:	expression,
				}

			if (type == 'fade') and (self.fades[self.getFadeId(par)]['end'] is not None):
				self.fades[self.getFadeId(par)]['end'] = float(self.fades[self.getFadeId(par)]['end'])
			
	def CreateEndSnap(self, par, end:float, time:float, type = 'snap', curve:str = 'lin', id = '', mode = 'CONSTANT', expression = None ):
		self.CreateTween( par, end, 0, "endsnap", curve = curve, id = id, mode = mode, expression=expression, delay = time)
		return
	
	def CreateStartSnap(self, par, end:float, time:float, type = 'snap', curve:str = 'lin', id = '' , mode = 'CONSTANT', expression = None):
			
		if mode == 'EXPRESSION':
			par.mode = ParMode[mode]
			par.expr = expression
		else:
			par.val = end
		self.fades.pop(self.getFadeId(par), None)
		
		return

	def StopFade(self,par):
		del self.fades[self.getFadeId(par)]

	def StopAllFades(self):
		self.fades = {}

	def ClearFades(self):
		self.fades.clear()

	def PrintFades(self):
		print(self.fades)