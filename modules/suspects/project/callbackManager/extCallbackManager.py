


'''Info Header Start
Name : extCallbackManager
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from functools import lru_cache
TDF = op.TDModules.mod.TDFunctions
import TDJSON

class extCallbackManager:
	"""
	extCallbackManager description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.pageName = 'Callbacks'
		self.callbackTemplate = self.ownerComp.op('default_callbacks')

	@property
	def owner(self):
		return self.ownerComp.par.Owner.eval()
	
	@property
	def moduleOperator(self):
		return self.owner.par.Callbacks.eval()
	
	@property
	def callbackModule(self):
		return self.moduleOperator.module
	  
	def Reset(self):
		self.owner.par.Callbacks = self.callbackTemplate

	def Refresh(self):
		self.Execute.cache_clear()

	def InitOwner(self):
		prefab = { parameter.name : TDJSON.parameterToJSONPar( parameter ) for parameter  in self.ownerComp.op("parameter_prefab").customPars }
		try:
			callbacks_par = TDJSON.addParameterFromJSONDict( self.owner, prefab["Callbacks"], replace = False )
			callbacks_par.val = self.owner.relativePath(self.callbackTemplate)
		except tdError:
			pass

		try:
			create_par = TDJSON.addParameterFromJSONDict( self.owner, prefab["Createcallbacks"], replace = False )
		except tdError:
			pass

	def empty_callback(self, *args, **kwargs):
		return
	
	@lru_cache(maxsize=None)
	def Execute(self, name):
		return getattr( self.callbackModule, name, self.empty_callback)

	def Do_Callback(self, name, *arguments, **keywordarguments):
		try:
			return self.Execute(name)(*arguments, **keywordarguments)
		except Exception as e:
			if self.ownerComp.par.Gracefulerror.eval(): 
				self.ownerComp.op("logger").Log( "Error during callback execution", e)
				return None
			raise e

	def CreateCallbacks(self, owner):
		new_callback_dat = owner.parent().copy(self.callbackTemplate, name = f"{owner.name}_callbacks")
		new_callback_dat.nodeX = owner.nodeX
		new_callback_dat.nodeY = owner.nodeY - 150
		new_callback_dat.dock = owner
		owner.par.Callbacks = new_callback_dat
		