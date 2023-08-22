




'''Info Header Start
Name : JsonConfig
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
import config_module, json
import pathlib

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
		self.Refresh_File()

	@property
	def Filepath(self):
		self.log("Generating Filepath")
		path = pathlib.Path( self.ownerComp.par.Filepath.eval() )
		path.parent.mkdir( parents=True, exist_ok=True )
		if self.ownerComp.par.Useenv.eval():
			path = path.with_stem(f"{self.ownerComp.par.Currentenv.eval()}_{info.baseName}")
		path.touch()
		return path

	def Refresh_File(self):
		self.log("Refreshing File")
		with open( self.Filepath, "rt" ) as configFile:
			self.Data = self.Load_From_Json( configFile.read() or "{}")
		if self.ownerComp.extensionsReady : self.ownerComp.cook( force = True )
		self.Save()

	def Save(self):
		self.log("Saving File")
		with open( self.Filepath, "wt" ) as configFile:
			configFile.write( self.Data.To_Json() )
		

	def Load_From_Json(self, json_string):
		self.log( "Loading Json String", json)
		return self.Load_From_Dict( json.loads( json_string))

	def Load_From_Dict(self, datadict:dict):
		schema = config_module.Collection(
			self.ownerComp.op("callbackManager").Execute("GetConfigSchema")( config_module.ConfigValue, config_module.CollectionDict, config_module.CollectionList) 
		)
		data = config_module.Collection( schema )
		data.Set( datadict )
		return data