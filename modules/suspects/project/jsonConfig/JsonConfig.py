'''Info Header Start
Name : JsonConfig
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''


import json
import pathlib

import config_module


class JsonConfig:
	"""
	JsonConfig description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log
		self.log("Init")
		
		self.ConfigModule = config_module
		self.LoadConfig()

		#backwards compatible 
		self.Refresh_File = self.LoadConfig

	@property
	def Filepath(self):
		self.log("Generating Filepath")
		currentEnv = self.ownerComp.par.Currentenv.eval()
		path = pathlib.Path( self.ownerComp.par.Filepath.eval() )
		path.parent.mkdir( parents=True, exist_ok=True )
		if self.ownerComp.par.Useenv.eval() and currentEnv:
			path = path.with_stem(f"{currentEnv}_{path.name}")
		path.touch()
		return path

	def readFileJson(self):
		with open( self.Filepath, "rt" ) as configFile:
			return configFile.read()
		
	def LoadConfig(self, configString = ""):
		self.log("Refreshing File")
		self.Data = self.loadFromJson( 
			configString or
			self.ownerComp.op("callbackManager").Do_Callback("GetConfigData") or
			self.readFileJson() or 
			"{}" )
		if self.ownerComp.extensionsReady : self.ownerComp.cook( force = True )
		self.Save()

	def Save(self):
		self.log("Saving File")
		if self.ownerComp.par.Exportschema.eval():
			self.saveSchema()
			self.Data["$schema"] = f"./" + str( self.Filepath.with_suffix(".schema.json" ).name )

		with open( self.Filepath, "wt" ) as configFile:
			configFile.write( self.Data.To_Json() )
	
	def saveSchema(self):
		self.log("Saving Schema")
		with open( self.Filepath.with_suffix(".schema.json" ), "wt" ) as schemaFile:
			schemaFile.write( json.dumps( self.Data._GetSchema(), indent = 1 ) )

	def loadFromJson(self, json_string):
		self.log( "Loading Json String", json)
		return self.loadFromDict( json.loads( json_string))

	def loadFromDict(self, datadict:dict):
		schema = config_module.Collection(
			self.ownerComp.op("callbackManager").Do_Callback("GetConfigSchema", config_module.ConfigValue, config_module.CollectionDict, config_module.CollectionList) or {}
		)
		data = config_module.Collection( schema )
		data.Set( datadict )
		return data