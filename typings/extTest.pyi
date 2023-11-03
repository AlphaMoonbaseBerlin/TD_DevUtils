class extTest:
    """
	THis is a ClassDoscstring.
	Multiline!
	+## one two Three
	"""

    def __init__(self, ownerComp):
        """THis is the docstring for a Constructor"""
        self.ownerComp = ownerComp
        self.unttyped = 1
        self.typed: int = 2
        self.inferredFromFunction = self.typedFunction(3)
        pass

    def typedFunction(self, value: int) -> str:
        pass

    def untypedFunction(self, value):
        pass

    def inferredFUnction(self, value):
        pass