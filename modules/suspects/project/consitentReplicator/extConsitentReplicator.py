

'''Info Header Start
Name : extConsitentReplicator
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
import tableUtils

class extConsitentReplicator:
	"""
	extConsitentReplicator description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.callback = self.ownerComp.op('callbackManager')
		if self.ownerComp.par.Active.eval(): 
			run( "me.Replicate()", fromOP=self.ownerComp, delayFrames = 1)
	@property
	def TemplateDAT(self):
		return self.ownerComp.par.Template.eval()
	
	def findReplicants(self):
		return tuple( self.ownerComp.par.Target.eval().findChildren( tags = [self.ownerComp.par.Replicatortag], maxDepth = 1 ) )
	
	def parseDatTemplate(self):
		templateList = tableUtils.tableToDict( self.TemplateDAT )
		namekey = self.ownerComp.par.Namekey.eval()
		return {
			tdu.legalName( item[ namekey ] ) : item for item in templateList
		}
	
	def Clear(self):
		for replicant in self.findReplicants():
			replicant.destroy()

	def Replicate(self, preClear = False):
		if preClear: self.Clear()
		template = self.parseDatTemplate()
		self.huntExistingReplicants(template)
		self.createMissingReplicants(template)
		return
		
	def huntExistingReplicants(self, template):
		for hunted in self.findReplicants():
			if hunted.name in template: continue
			hunted.destroy()
	
	def createMissingReplicants(self, template):
		target = self.ownerComp.par.Target.eval()
		for replicantName, replicantTemplate in template.items():
			if target.op(replicantName): continue
			self.createReplicant( replicantTemplate, target )
			
	def createReplicant(self, name:str, template:dict, target):
		self.callback.Do_Callback( "onPreCreate", template, self.ownerComp )
		newReplicant = target.copy( self.ownerComp.par.Blueprint.eval(), name = name)
		newReplicant.tags.add( self.ownerComp.par.Replicatortag.eval() )
		self.callback.Do_Callback( "onNewReplicant", newReplicant, template, self.ownerComp )
			
			
			
			
			
			
			
			
			
			
			
			
			
			