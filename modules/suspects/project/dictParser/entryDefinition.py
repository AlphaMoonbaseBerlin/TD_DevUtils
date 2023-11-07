'''Info Header Start
Name : entryDefinition
Author : wieland@MONOMANGO
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from dataclasses import dataclass, field
from typing import Callable
log = op("logger").Log

class EntryRequired( Exception):
    pass

def emptyReturn(value):
    return str( value )

@dataclass
class EntryDefinition:
    """Generates a EntryDefinition for the parser."""
    name            : str                   = field()
    
    parseFunction   : Callable[[any], any]  = field(repr = False)
    returnFunction  : Callable[[str], any]  = field(repr = False, default=emptyReturn)
    
    default         : str   = field( default = "" )
    required        : bool  = field( default = False )
    
    def parse( self, data:dict ):
        try:
            return self.parseFunction( data )
        except KeyError as e:
            log( e )
            if self.required: raise EntryRequired( e.args )
            else: return self.default

    def unparse(self, value:str):
        return self.returnFunction( value )