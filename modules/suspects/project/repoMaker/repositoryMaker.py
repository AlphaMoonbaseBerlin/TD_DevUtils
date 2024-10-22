'''Info Header Start
Name : repositoryMaker
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''

class repositoryMaker:
	"""
	repositoryMaker description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Reset(self):
		self.repoParameter.val = self.prefabOperator

	def InitOwner(self):
		page = self.find_repo_page()
		opParameter = page.appendOP( 		
			self.OperatorParName,
			label = self.ownerName, 
			replace=True)
		opParameter.val = self.prefabOperator
		opParameter[0].startSection  = True
		page.appendPulse( 	
			self.CreateParName,
			label = "Create", 
			replace=True)
		return
	
	@property
	def OperatorParName(self):
		return f"{self.ownerName.capitalize()}repo"

	@property
	def CreateParName(self):
		return f"{self.ownerName.capitalize()}repocreate"

	@property
	def Owner(self):
		return self.ownerComp.par.Owner.eval()

	@property
	def ownerName(self):
		return self.ownerComp.par.Name.eval()

	@property 
	def repoParameterVal(self):
		return self.repoParameter.eval()
	
	@property
	def repoParameter(self):
		return self.Owner.par[self.OperatorParName]
	
	@property
	def Repo(self):
		if self.Initialized:
			if self.ownerComp.par.Autocreate.eval() and self.repoParameterVal == self.prefabOperator: 
				self.Create_Repo()
			
			if self.repoParameter.eval() is None: 
				# This fixes the NONE Definition for one frame on delete but results in other unexpected behaviour.
				# Needs to be tested!
				self.Reset()

			return self.repoParameterVal
		return None

	@property
	def prefabOperator(self):
		return self.ownerComp.par.Prefab.eval()

	@property
	def Initialized(self):
		return hasattr( self.Owner.par, self.OperatorParName )

	# def Reevaluate(self):
	# 	if self.Owner.par[ self.OperatorParName ].eval(): return
	# 	self.Owner.par[ self.OperatorParName ].val = self.prefabOperator
	# 	return

	def Create_Repo(self):
		x_offset 	= 0
		for docked_op in self.Owner.docked:
			x_offset += docked_op.nodeWidth + 20
		repo 		= self.Owner.parent().copy( self.prefabOperator, name = f"{self.Owner.name}_{self.ownerName}")
		repo.nodeX 	= self.Owner.nodeX + x_offset
		repo.nodeY 	= self.Owner.nodeY - ( repo.nodeHeight + 20 )
		repo.dock 	= self.Owner
		self.Owner.par[self.OperatorParName].val = repo
		return

	def find_repo_page(self):
		pagename = self.ownerComp.par.Pagename.eval() or "Repository"
		for page in self.Owner.customPages:
			if page.name == pagename:
				return page
		return self.Owner.appendCustomPage( pagename )
	