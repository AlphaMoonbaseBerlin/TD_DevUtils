'''Info Header Start
Name : extStubser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''
import ast
from pathlib import Path
import re
from stubsTransformer import StubsTransformer

debug = op("logger").Log

class extStubser:
	"""
	A Utility to automaticaly generate stubs for touchdesigner Extensions and modules.
	"""
	def __init__(self, ownerComp:COMP):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Stubify(self, input:str, includePrivate:bool = False, includeUnpromoted:bool = True) -> str:
		"""Generate a stubified String of a module, removing all unnecesarry elements of functions."""
		data = ast.parse(input)
		transformedData = StubsTransformer( includePrivate, includeUnpromoted).visit( data )
		
		return ast.unparse(transformedData)
	
	def _placeTyping(self, stubsString:str, name:str):
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

	
	def StubifyDat(self, target:textDAT, includePrivate:bool = False, includeUnpromoted:bool = True):
		self._placeTyping(
			self.Stubify(
				target.text, 
				includePrivate=includePrivate, 
				includeUnpromoted=includeUnpromoted), 
			target.name )

	def StubifyComp(self, target:COMP, depth = 1, tag = "stubser", includePrivate:bool = False, includeUnpromoted:bool = True):
		for child in target.findChildren( 
				tags=tdu.split( self.ownerComp.par.Tag.eval() ), 
				type=textDAT, 
				maxDepth = depth ):
			
			self.StubifyDat( 
				child, 
				includePrivate=includePrivate, 
				includeUnpromoted=includeUnpromoted )
			
	def _findParPage(self, name):
		pagename = name
		owner = self.ownerComp.par.Owner.eval()
		for page in owner.customPages:
			if page.name == pagename:
				return page
		return owner.appendCustomPage( pagename )

	def InitOwner(self):
		page = self._findParPage("Stubser")
		page.appendPulse( 	
			"Deploystubs",
			label 		= "Deploy Stubs",
			replace		= True )
		return
	