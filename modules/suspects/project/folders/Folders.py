
'''Info Header Start
Name : Folders
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
from shortcut import path_shortcut
import tempfile

class Folders:
	"""
	Folders description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
		for row in self.ownerComp.op("data").rows():
			setattr(self, row[0].val, path_shortcut(row[1].val))

