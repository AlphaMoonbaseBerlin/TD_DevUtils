'''Info Header Start
Name : extQrCode
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''
import io
class extQrCode:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		
		self.qrcode = self.ownerComp.op('olib_dependancy').Get_Component().Import_Module("qrcode", pip_name = "qrcode[pil]" )
		

	def Create_QrCode(self, target):
		qr_image = self.qrcode.make( 	target, 
										box_size = self.ownerComp.par.Fieldsize.eval(), 
										border = self.ownerComp.par.Bordersize.eval() )
		debug( qr_image.size )
		self.ownerComp.op('qr_text').text = target
		byteIO = io.BytesIO()
		qr_image.save( byteIO, format = "PNG")
		self.ownerComp.vfs["qrcode.png"].destroy()
		self.ownerComp.vfs.addByteArray( bytearray( byteIO.getvalue() ), "qrcode.png" )
		self.ownerComp.op('moviefilein1').cook( force = True)