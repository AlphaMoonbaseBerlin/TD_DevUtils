"""Info Header Start
Name : extStubser
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End"""
import ast
from pathlib import Path

class extStubser:
    """
	A Utility to automaticaly generate stubs for touchdesigner Extensions and modules.
	"""

    def __init__(self, ownerComp: COMP):
        self.ownerComp = ownerComp
        pass

    def Stubify(self, input: str) -> str:
        """Generate a stubified String of a module, removing all unnecesarry elements of functions."""
        pass

    def placeTyping(self, stubsString: str, name: str):
        """Export the given stubs string in to a file and add it as a builtins!"""
        pass

    def StubifyDat(self, target: textDAT):
        pass

    def StubifyComp(self, target: COMP):
        pass

    def findParPage(self, name):
        pass

    def InitOwner(self):
        pass