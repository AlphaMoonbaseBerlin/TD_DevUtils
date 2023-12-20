'''Info Header Start
Name : extDictParser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''


from functools import lru_cache
from entryDefinition import EntryDefinition
from typing import List, Union, Dict

entryIndex = Union[str, int]

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
		return self.ownerComp.op("output")
	
	@property
	def dataTable(self) -> tableDAT:
		return self.ownerComp.op("data") 
	
	def Refresh(self):
		self.getDefintion.cache_clear()
		self.getDefintion()
		return
	
	def Clear(self, keepHeader = True):
		self.dataTable.clear(keepFirstRow = keepHeader)

	@lru_cache(maxsize=1)
	def getDefintion(self):
		definitionList:List[EntryDefinition] = self.ownerComp.op("callbackManager").Do_Callback(
			"GetDefinition", 
			EntryDefinition, 
			self.ownerComp
		)
		if self.ownerComp.par.Autoreset.eval(): 
			self.Clear( keepHeader = False )
			self.dataTable.appendRow([
				definitionItem.name for definitionItem in definitionList
			])
		return definitionList
	
	def AddDict(self, data:dict, unique = True):
		dataset = [ item.parse( data ) for item in self.getDefintion() ]
		if not dataset: raise Exception("No Definition defined!")
		if unique and self.dataTable.row( dataset[0] ):
			self.dataTable.replaceRow( dataset[0], dataset )
		else:
			self.dataTable.appendRow( dataset )

	def AddDicts(self, data:List[dict], unique = True):
		for item in data:
			self.AddDict( item, unique=unique )


	def GetRow(self, rowIndex:entryIndex):
		return {
			item.name : item.unparse( str( self.outputTable[ rowIndex, item.name] ) ) for item in self.getDefintion() 
		}
	
	def GetValue(self, rowIndex:entryIndex, itemIndex:entryIndex) -> Dict[str, any]:
		"""Return a dictionary of the parsed row!"""
		targetCell:Cell = self.outputTable[ rowIndex, itemIndex ]
		if not targetCell: return None
		entryDefinition:EntryDefinition = self.getDefintion[targetCell.col]
		return entryDefinition.unparse( targetCell.val )
	
	def SearchRows(self, searchValue:str, searchCol:entryIndex) -> List[entryIndex]:
		"""This loads the complete row, which is def not ideal, but usable. Use Index-Tables for quicker search?"""
		foundCells = [result for result in tdu.match(searchValue, self.outputTable.col(searchCol)[1:] )]
		return [
			self.outputTable[ cell.row, 0].val for cell in foundCells
		]