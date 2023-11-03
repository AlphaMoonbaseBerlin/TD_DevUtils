'''Info Header Start
Name : extStubser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
import ast
from pathlib import Path
import re


debug = op("logger").Log

class extStubser:
	"""
	A Utility to automaticaly generate stubs for touchdesigner Extensions and modules.
	"""
	def __init__(self, ownerComp:COMP):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Stubify(self, input:str) -> str:
		"""Generate a stubified String of a module, removing all unnecesarry elements of functions."""
		data = ast.parse(input)
		for node in ast.walk(data):
			emptyBody = []
			# let's work only on functions & classes definitions
			if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
				#Just do FunctionDefinitions!
				continue
			if not len(node.body):
				#If not elements are in the node, skip.
				continue
			
			if hasattr(node.body[0], 'value') and isinstance(node.body[0].value, ast.Str):
				#Lets assume this ies a doscstring!
				emptyBody = node.body[:1]

			if node.name == "__init__":
				for item in node.body:
					
					if isinstance(item, ast.Assign) and [ target for target in item.targets if isinstance(target, ast.Attribute)]:
						emptyBody.append( item )
					if isinstance(item, ast.AnnAssign) and isinstance( item.target, ast.Attribute):
						emptyBody.append( item )
			node.body = emptyBody + [ ast.Pass() ]
		return ast.unparse(data)
	
	def placeTyping(self, stubsString:str, name:str):
		"""Export the given stubs string in to a file and add it as a builtins!"""
		debug("Placing Typings", name)
		builtinsFile = Path("typings", "__builtins__.pyi")
		builtinsFile.parent.mkdir( exist_ok=True, parents=True)
		builtinsFile.touch(exist_ok=True)

		currentBuiltinsText = builtinsFile.read_text()
		if not re.search(f"from {name} import *", currentBuiltinsText): 
			with builtinsFile.open("t+a") as builtinsFileHandler:
				builtinsFileHandler.write(f"\nfrom { name} import *")
		
		stubsFile = Path("typings", name).with_suffix( ".pyi")
		
		stubsFile.touch( exist_ok=True)
		stubsFile.write_text( stubsString )

	
	def StubifyDat(self, target:textDAT):
		debug( "Stubifying Dat", target.name)
		self.placeTyping(self.Stubify(target.text), target.name )

	def StubifyComp(self, target:COMP):
		debug( "Stubifying COMP", target.name )
		for child in target.findChildren( tags=["stubser"], type=textDAT ):
			self.StubifyDat( child )
			
	def findParPage(self, name):
		pagename = name
		owner = self.ownerComp.par.Owner.eval()
		for page in owner.customPages:
			if page.name == pagename:
				return page
		return owner.appendCustomPage( pagename )

	def InitOwner(self):
		page = self.findParPage("Stubser")
		page.appendPulse( 	
			"Deploystubs",
			label 		= "Deploy Stubs",
			replace		= True )
		return
	