'''Info Header Start
Name : entryDefinition
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from dataclasses import dataclass
from typing import Callable
log = op("logger").Log

class EntryRequired( Exception):
    pass

@dataclass
class EntryDefinition:
    name        : str
    parseFunction: Callable
    
    default     : str   = ""
    required    : bool  = False
    

    def parse( self, data:dict ):
        try:
            return self.parseFunction( data )
        except KeyError as e:
            log( e )
            if self.required: raise EntryRequired( e.args )
            else: return self.default

