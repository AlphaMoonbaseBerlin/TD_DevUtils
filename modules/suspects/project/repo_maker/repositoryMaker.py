
'''Info Header Start
Name : repositoryMaker
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

class repositoryMaker:
	"""
	repositoryMaker description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Init_Owner(self):
		page = self.find_repo_page()
		op_parameter = page.appendOP( 		
			self.Operator_Par_Name,
			label = self.Name, 
			replace=True)
		op_parameter.val = self.Prefab
		op_parameter[0].startSection  = True
		page.appendPulse( 	
			self.Create_Par_Name,
			label = "Create", 
			replace=True)
		return
	@property
	def Operator_Par_Name(self):
		return f"{self.Name.capitalize()}repositorie"

	@property
	def Create_Par_Name(self):
		return f"{self.Name.capitalize()}create"

	@property
	def Owner(self):
		return self.ownerComp.par.Owner.eval()

	@property
	def Name(self):
		return self.ownerComp.par.Name.eval()

	@property 
	def repo_par(self):
		return self.Owner.par[self.Operator_Par_Name].eval()

	@property
	def Repo(self):
		if self.Initialized:
			if self.ownerComp.par.Autocreate.eval() and self.repo_par == self.Prefab: self.Create_Repo()
			return self.repo_par
		return None

	@property
	def Prefab(self):
		return self.ownerComp.par.Prefab.eval()

	@property
	def Initialized(self):
		return hasattr( self.Owner.par, self.Operator_Par_Name )

	def Reevaluate(self):
		if self.Owner.par[ self.Operator_Par_Name ].eval(): return
		self.Owner.par[ self.Operator_Par_Name ].val = self.Prefab
		return

	def Create_Repo(self):
		x_offset 	= 0
		for docked_op in self.Owner.docked:
			x_offset += docked_op.nodeWidth + 20
		repo 		= self.Owner.parent().copy( self.Prefab, name = f"{self.Owner.name}_{self.Name}")
		repo.nodeX 	= self.Owner.nodeX + x_offset
		repo.nodeY 	= self.Owner.nodeY - ( repo.nodeHeight + 20 )
		repo.dock 	= self.Owner
		self.Owner.par[self.Operator_Par_Name].val = repo
		return

	def find_repo_page(self):
		pagename = self.ownerComp.par.Pagename.eval() or "Repositorie"
		for page in self.Owner.customPages:
			if page.name == pagename:
				return page
		return self.Owner.appendCustomPage( pagename )
	