


'''Info Header Start
Name : extStore
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

class extStore:
	"""
	extStore description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.parseTable( self.ownerComp.op('store_table') )
		
	def parseTable(self, table):
		for row in table.rows()[1:]:
			row[0].val = tdu.legalName( row[0].val ).capitalize()
			row[1].val = self.getPath( self.getOperator( row[1].val ) )
			setattr( self, row[0].val, self.getOperator( row[1].val ) )
			
	def AddOp(self, operator, shortcut_name = None):
		shortcut_name = operator.name if shortcut_name is None else shortcut_name
		path = self.getPath( operator )
		self.ownerComp.op('store_table').appendRow( [shortcut_name.capitalize(), path] )
	
	def getOperator(self, path):
		self.ownerComp.par.Placeholder.val = path
		return self.ownerComp.par.Placeholder.eval()
		
	def getPath(self, op):
		if self.ownerComp.par.Relative.eval(): return self.relativePath( op )
		return self.absolutePath( op )
	
	def relativePath(self, op):
		return self.ownerComp.relativePath( op )
		
	def absolutePath(self, op):
		return op.path