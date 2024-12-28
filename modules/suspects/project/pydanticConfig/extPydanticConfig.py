'''Info Header Start
Name : extPydanticConfig
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

from functools import lru_cache

try:
	import pydantic
except:
	pass

class extPydanticConfig:
	"""
	extPydanticConfig description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.pip = self.ownerComp.op("td_pip")
		self.Pydantic:"pydantic" = self.pip.ImportModule("pydantic")

	@property
	def Data(self):
		return self._Data(
			self.ownerComp.op("exampleConfig").text
		)
	
	@lru_cache(maxsize=1)
	def _Data(self, jsonText):
		schema:"pydantic.BaseModel" = self.ownerComp.op("callbackManager").Do_Callback(
			"GetSchema", self.ownerComp
		)
		
		validatedItem = schema.model_validate_json( jsonText )
		for fieldName, fieldInfo in validatedItem.model_fields.items():
			setattr( validatedItem, fieldName, tdu.Dependency(
				getattr( validatedItem , fieldName)
			))
		return validatedItem