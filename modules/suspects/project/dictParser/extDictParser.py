'''Info Header Start
Name : extDictParser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
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

		# Backwards Compatible!
		self.AddDict = self.AddItem
		self.AddDicts = self.AddItems
		self.Refresh()

	@property
	def outputTable(self) -> tableDAT:
		return self.ownerComp.op("output")
	
	@property
	def dataTable(self) -> tableDAT:
		return self.ownerComp.op("repoMaker").Repo 
	
	@property
	def NumItems(self) -> int:
		return self.dataTable.numRows - 1

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
		return { item.name : item for item in definitionList }
	
	def AddItem(self, data:dict, unique = True):
		"""
			Passes a dict to the parser-functions and saves it to the table.
			When unique is enabled it will overwrite existing entries with the same
			primary key.
		"""
		dataset = [ item.parse( data ) for item in self.getDefintion().values() ]
		if not dataset: raise Exception("No Definition defined!")
		if unique and self.dataTable.row( dataset[0] ):
			self.dataTable.replaceRow( dataset[0], dataset )
		else:
			self.dataTable.appendRow( dataset )

	def UpdateItem(self, itemId:Union[str, int], dataset:dict):
		"""
			Replaces the data in the table at the given ID with the dataset given.
		"""
		self.dataTable.replaceRow( itemId, dataset )

	def AddItems(self, data:List[dict], unique = True):
		"""
			Ads a list of dicts.
		"""
		for item in data:
			self.Additem( item, unique=unique )


	def GetRow(self, rowIndex:entryIndex):
		"""Deprecated, used GetItem instead"""
		return {
			item.name : item.unparse( str( self.outputTable[ rowIndex, item.name] ) ) for item in self.getDefintion().values() 
		}
	
	def GetItem(self, itemId:str, rows = "*") -> dict:
		"""
			Get a single items as a dict.
		"""
		itemDefinition = self.getDefintion()
		fetchNames = tdu.match(
			rows, list(itemDefinition.keys())
		)
		result = {
			itemDefinition[name].name : itemDefinition[name].unparse( 
				str( self.outputTable[ itemId, itemDefinition[name].name] ) 
			) for name in fetchNames
		}
		result["_tableIndex"] = self.outputTable[ itemId, 0].row
		return result
	
	def DeleteItem(self, itemId:str):
		"""
			Delete an item based on the ID. Returns True or False depending of success.
		"""
		try:
			self.dataTable.deleteRow( str(itemId) )
			return True
		except tdError:
			return False

	def SearchItems(self, key = lambda value: True, rows = "*") -> List[Dict]:
		"""
			Search Items in the table based on the key-function returning true or false.
			Use rows arguments to filter returned data.
		"""
		returnData = []
		for idCell in self.dataTable.col(0)[1:]:
			item = self.GetItem( idCell.val, rows = rows )
			if key(item): returnData.append( item )
		return returnData

	def SortTable(self, key = lambda row: row[0], reverse = False) -> bool:
		"""
			Sorts the table based on the key-function. This works on the table
			holding the data and does not change the data.
		"""
		sortedData = sorted(
    		[[cell.val for cell in row] for row in self.dataTable.rows()[1:]], 
			key = key,
			reverse=reverse
		)
		self.dataTable.clear(keepFirstRow = True)
		self.dataTable.appendRows( sortedData )