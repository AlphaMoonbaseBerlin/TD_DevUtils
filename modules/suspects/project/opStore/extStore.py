


'''Info Header Start
Name : extStore
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

class opProperty:
	def __init__(self, operator):
		self._operator = operator

	
	def __get__(self, instance, owner):
		debug(instance, owner)
		return self._operator
	
	def __call__(self, *args, **kwds):
		return self._operator.op(args[0])

class extStore:
	"""
	extStore description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.parseTable( self.storeTable )
	
	@property
	def storeTable(self):
		return self.ownerComp.op("repoMaker").Repo

	def parseTable(self, table):
		for row in table.rows()[1:]:
			targetOperator = self.getOperator( row[1].val )
			targetName = tdu.legalName( row[0].val ).capitalize()
			row[0].val = targetName
			row[1].val = self.getPath( targetOperator )

			setattr( self, targetName, opProperty( targetOperator) )
			
	def AddOp(self, operator, shortcut_name = None):
		shortcut_name = operator.name if shortcut_name is None else shortcut_name
		path = self.getPath( operator )
		self.storeTable.appendRow( [shortcut_name.capitalize(), path] )
	
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