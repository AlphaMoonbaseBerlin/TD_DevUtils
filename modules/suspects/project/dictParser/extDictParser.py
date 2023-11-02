'''Info Header Start
Name : extDictParser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from functools import lru_cache
from entryDefinition import EntryDefinition
from typing import List
class extDictParser:
	"""
	extDictParser description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.Refresh()

	@property
	def outputTable(self) -> tableDAT:
		return self.ownerComp.op("data")

	def Refresh(self):
		self.getDefintion.cache_clear()
		self.getDefintion()
		return
	
	def Clear(self):
		self.outputTable.clear(keepFirstRow = True)

	@lru_cache(maxsize=1)
	def getDefintion(self):
		definitionList:List[EntryDefinition] = self.ownerComp.op("callbackManager").Do_Callback(
			"GetDefinition", 
			EntryDefinition, 
			self.ownerComp
		)
		self.outputTable.clear()
		self.outputTable.appendRow([
			definitionItem.name for definitionItem in definitionList
		])
		return definitionList
	
	def AddDict(self, data:dict, unique = True):
		self.outputTable.appendRow([
			item.parse( data ) for item in self.getDefintion()
		])

	def AddDicts(self, data:List[dict]):
		for item in data:
			self.AddDict( item )
