
'''Info Header Start
Name : extCallbackManager
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 3
Savetimestamp : 2023-07-13T12:34:49.587234
Saveorigin : Project.toe
Saveversion : 2022.28040
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
		self.callback_module = None
		TDF.createProperty(self, 'Module_Op', value=self.callbackTemplate, dependable=True,
						   readOnly=False)

		if hasattr( self.ownerComp.par.Owner.eval().par, "Callbacks"):
			module_op = self.ownerComp.par.Owner.eval().par.Callbacks.eval() or op('default_callbacks')
		else:
			module_op = op('default_callbacks')
			
		module_path = module_op.path
		self.init_callback_module( module_path )

	def init_callback_module(self, path):
		self.Module_Op = op( path )
		self.callback_module = mod( path )
		self.Execute.cache_clear()
		return

	def InitOwner(self, owner):
		prefab = { parameter.name : TDJSON.parameterToJSONPar( parameter ) for parameter  in self.ownerComp.op("parameter_prefab").customPars }
		
		try:
			callbacks_par = TDJSON.addParameterFromJSONDict( owner, prefab["Callbacks"], replace = False )
			callbacks_par.val = owner.relativePath(self.callbackTemplate)
		except tdError:
			pass

		try:
			create_par = TDJSON.addParameterFromJSONDict( owner, prefab["Createcallbacks"], replace = False )
		except tdError:
			pass
		
			
		
		return
		#page = owner.appendCustomPage(self.pageName)
		#page.appendPulse('Createcallbacks', label = 'Create Callbacks', replace = True)
		#datpar = getattr( owner.par, "Callbacks", page.appendDAT('Callbacks', replace = True)[0] )
		#datpar.readOnly = True
		#callbackpath = owner.relativePath(self.callbackTemplate)
		#datpar.val = datpar.eval() or callbackpath

	def empty_callback(self, *args, **kwargs):
		return
	
	@lru_cache(maxsize=None)
	def Execute(self, name):
		return getattr( self.callback_module, name, self.empty_callback)

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
		