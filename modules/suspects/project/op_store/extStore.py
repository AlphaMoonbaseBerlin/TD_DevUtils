'''Info Header Start
Name : extStore
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 2
Savetimestamp : 2023-08-15T13:24:15.618142
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
		self.Parse_Table( self.ownerComp.op('store_table') )
		
	def Parse_Table(self, table):
		for row in table.rows()[1:]:
			row[0].val = tdu.legalName( row[0].val ).capitalize()
			row[1].val = self.get_path( self.get_op( row[1].val ) )
			setattr( self, row[0].val, self.get_op( row[1].val ) )
			
	def Add_Op(self, operator, shortcut_name = None):
		shortcut_name = operator.name if shortcut_name is None else shortcut_name
		path = self.get_path( operator )
		self.ownerComp.op('store_table').appendRow( [shortcut_name.capitalize(), path] )
	
	def get_op(self, path):
		self.ownerComp.par.Placeholder.val = path
		return self.ownerComp.par.Placeholder.eval()
		
	def get_path(self, op):
		if self.ownerComp.par.Relative.eval(): return self.relative_path( op )
		return self.absolute_path( op )
	
	def relative_path(self, op):
		return self.ownerComp.relativePath( op )
		
	def absolute_path(self, op):
		return op.path