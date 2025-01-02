'''Info Header Start
Name : extTweenChop
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

class extTweenChop:
	"""
	extTweenChop description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.tweener = self.ownerComp.op("remote_dependency").GetGlobalComponent()

	def InvokeTween(self, target, targetvalue = None, time = None, curve = None):
		seqBlock = None
		if isinstance( target, Par ):
			seqBlock = target.sequenceBlock
		elif isinstance( target, int):
			self.ownerComp.seq[target]
		elif isinstance( target, str):
			for block in self.ownerComp.seq:
				if block.par.Name.eval() == target:
					seqBlock = block
					break
				else:
					return
		else: return
		self.tweener.AbsoluteTween(
			seqBlock.par.Value,
			seqBlock.par.Targetvalue.eval() if targetvalue is None else targetvalue,
			seqBlock.par.Time.eval() if time is None else time,
			curve = seqBlock.par.Curve.eval() if curve is None else time
		)
		return
	
	
	