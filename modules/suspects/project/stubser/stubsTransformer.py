'''Info Header Start
Name : stubsTransformer
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''
import ast

class StubsTransformer(ast.NodeTransformer):
	def __init__(self, includePrivate:bool, includeUnpromoted:bool) -> None:
		super().__init__()
		self.includePrivate = includePrivate
		self.includeUnpromoted = includeUnpromoted

	def visit_FunctionDef(self, node):
		emptyBody = []
		if not len(node.body): return node
			
			#We might not want to expose private functions. So lets not do that. Easy.
		if (not self.includePrivate) and node.name.startswith("_") and node.name != "__init__": 
			return None
				
		#To make live easier for users, lets also enable just promoted methods.
		if (not self.includeUnpromoted) and node.name[0].islower(): 
			return None
				
		#check if first element is a string, if so we simply assume that it is a dosctring.
		if hasattr(node.body[0], 'value') and isinstance(node.body[0].value, ast.Str):
			emptyBody = node.body[:1]

		#If we assign members to a in an init-function, we need to make sure that we keep them, otherwise they get lost.
		if node.name == "__init__":
			for item in node.body:
				#TO DO: We should also check if we assign private or unpromoted elements.
				if isinstance(item, ast.Assign) and [ target for target in item.targets if isinstance(target, ast.Attribute)]:
					emptyBody.append( item )
				if isinstance(item, ast.AnnAssign) and isinstance( item.target, ast.Attribute):
					emptyBody.append( item )
		node.body = emptyBody + [ ast.Pass() ]
		return node
	visit_AsyncFunctionDef = visit_FunctionDef