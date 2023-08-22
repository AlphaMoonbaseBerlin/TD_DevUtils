'''Info Header Start
Name : EmittingInit
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

class EmittingInit:
	"""
	EmittingInit description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		self.ownerComp.op("Emitter").Attach_Emitter(self)

	def Run(self):
		self.ownerComp.op("timer1").par.start.pulse()
		