'''Info Header Start
Name : extDictParser
Author : wieland@MONOMANGO
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
		dataset = [ item.parse( data ) for item in self.getDefintion() ]
		if not dataset: raise Exception("No Definition defined!")
		if unique and self.outputTable.row( dataset[0] ):
			self.outputTable.replaceRow( dataset[0], dataset )
		else:
			self.outputTable.appendRow( dataset )

	def AddDicts(self, data:List[dict], unique = True):
		for item in data:
			self.AddDict( item, unique=unique )


	def GetRow(self, rowIndex):
		return {
			item.name : item.unparse( str( self.outputTable[ rowIndex, item.name] ) ) for item in self.getDefintion() 
		}