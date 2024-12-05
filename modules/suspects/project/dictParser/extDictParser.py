'''Info Header Start
Name : extDictParser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
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
	
	def AddItem(self, data:dict, unique = True, _dataTable = None):
		"""
			Passes a dict to the parser-functions and saves it to the table.
			When unique is enabled it will overwrite existing entries with the same
			primary key.
		"""
		dataTable = _dataTable or self.dataTable
		dataset = [ item.parse( data ) for item in self.getDefintion().values() ]
		if not dataset: raise Exception("No Definition defined!")
		if unique and dataTable.row( dataset[0] ):
			dataTable.replaceRow( dataset[0], dataset )
		else:
			dataTable.appendRow( dataset )

	def UpdateItem(self, itemId:Union[str, int], dataset:dict, _dataTable = None):
		"""
			Replaces the data in the table at the given ID with the dataset given.
		"""
		dataTable = _dataTable or self.dataTable
		dataTable.replaceRow( itemId, dataset )

	def AddItems(self, data:List[dict], unique = True, _dataTable = None):
		"""
			Ads a list of dicts.
		"""
		for item in data:
			self.Additem( item, unique=unique, _dataTable = _dataTable )


	def GetRow(self, rowIndex:entryIndex):
		"""Deprecated, used GetItem instead"""
		return {
			item.name : item.unparse( 
				str( self.outputTable[ rowIndex, item.name] ) 
			) for item in self.getDefintion().values() 
		}
	
	def GetItem(self, itemId:str, rows = "*", _dataTable = None) -> dict:
		"""
			Get a single items as a dict.
		"""
		outputTable = _dataTable or self.outputTable

		itemDefinition = self.getDefintion()
		fetchNames = tdu.match(
			rows, list(itemDefinition.keys())
		)
		result = {
			itemDefinition[name].name : itemDefinition[name].unparse( 
				str( outputTable[ itemId, itemDefinition[name].name] ) 
			) for name in fetchNames
		}
		result["_tableIndex"] = outputTable[ itemId, 0].row
		return result
	
	def DeleteItem(self, itemId:str, _dataTable = None):
		"""
			Delete an item based on the ID. Returns True or False depending of success.
		"""
		try:
			dataTable = _dataTable or self.dataTable
			dataTable.deleteRow( str(itemId) )
			return True
		except tdError:
			return False

	def SearchItems(self, key = lambda value: True, rows = "*", _dataTable = None) -> List[Dict]:
		"""
			Search Items in the table based on the key-function returning true or false.
			Use rows arguments to filter returned data.
		"""
		dataTable = _dataTable or self.dataTable
		returnData = []
		for idCell in dataTable.col(0)[1:]:
			item = self.GetItem( idCell.val, rows = rows )
			if key(item): returnData.append( item )
		return returnData

	def SortTable(self, key = lambda row: row[0], reverse = False, _dataTable = None) -> bool:
		"""
			Sorts the table based on the key-function. This works on the table
			holding the data and does not change the data.
		"""
		dataTable = _dataTable or self.dataTable
		sortedData = sorted(
    		[[cell.val for cell in row] for row in dataTable.rows()[1:]], 
			key = key,
			reverse=reverse
		)
		dataTable.clear(keepFirstRow = True)
		dataTable.appendRows( sortedData )