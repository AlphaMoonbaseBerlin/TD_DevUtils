'''Info Header Start
Name : config_module
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

_debug = op("logger").Log
class _copyCallable:
    def __call__(self):
        return copy.deepcopy( self )

from collections.abc import Iterable
def _typeToString(typeObject):
    if typeObject is float: return "number"
    if typeObject is int : return "integer"
    if typeObject is str : return "string"
    if typeObject is bool: return "boolean"
    return "undefined"

def _parseTypes( typesOrType ):
    if not isinstance(typesOrType, Iterable):
        typesOrType = [typesOrType]
    return [ _typeToString( typeObject) for typeObject in typesOrType ]



class EnumValue(_copyCallable):
    """An Enum value where the given values need to satisfy the allowedValue passed on init."""
    def _to_json(self):
        return self.Value
    
    def __repr__(self) -> str:
        return str( self.value.val )
    
    def __init__(self, 
                default = "", 
                allowedValues = [],
                validator = lambda value: True, 
                comment = "", 
                parser = None ):
        self.comment = comment
        self.validator = validator
        self.value = tdu.Dependency(None)
        self.parser = parser or type(default)
        self._allowedValues = allowedValues
        self.Set( default )

    def _validate(self, value):
        if not value in self._allowedValues:
            return False, f"Invalid Value. Needs to be one of {self._allowedValues}"
        if not self.validator( value ):
            return False, f"Validation requirement not satisfied"
        return True, "Pass"
        
    def Set(self, value):
        _debug( "Set ConfigValue", value)
        valid, errorstring = self._validate( value )
        if not valid:
            return False
        parsed_value = self.parser( value )
        self.value.val = parsed_value
        self.value.modified()

    @property
    def Dependency(self):
        return self.value
    
    @property
    def Value(self):
        return self.value.val

    def _GetSchema(self):
        return {
            "description" : self.comment,
            "enum" : self._allowedValues
        }

class ConfigValue(_copyCallable):
    """A generic value which allows to be bound to. Use .Value to refference the Value
    and .Dependency to bind to the value."""
    def _to_json(self):
        return self.Value
    def __repr__(self) -> str:
        return str( self.value.val )
    
    def __init__(self, 
                default = "", 
                validator = lambda value: True, 
                comment = "", 
                parser = None,
                typecheck = None):
        self.comment = comment
        self.validator = validator
        self.value = tdu.Dependency(None)
        self.parser = parser or type(default)
        self.typecheck = typecheck or type(default)
        self.Set( default )

    def _validate(self, value):
        if not isinstance(value, self.typecheck):
            return False, f"Invalid type. Expected {self.typecheck} got {type(value)}"
        if not self.validator( value ):
            return False, f"Validation requirement not satisfied"
        return True, "Pass"
        
    def Set(self, value):
        _debug( "Set ConfigValue", value)
        valid, errorstring = self._validate( value )
        if not valid:
            return False
        parsed_value = self.parser( value )
        self.value.val = parsed_value
        self.value.modified()

    @property
    def Dependency(self):
        return self.value
    
    @property
    def Value(self):
        return self.value.val

    def _GetSchema(self):
        return {
            "description" : self.comment,
            "type" : _parseTypes( self.typecheck )
        }



class CollectionDict(dict, _copyCallable):
    """A dictionary where all given keys need to be satisfied."""
    def __init__(self, items:dict = None, comment = ""):
        self.comment = comment
        if items: self.update( items )
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError from e
    
    def Set(self, data):
        _debug( "Set CollectionDict", data)
        for key, item in data.items():
            if key in self: self[key].Set( item )

    def _GetSchema(self):
        return {
            "description" : self.comment,
            "type" : "object",
            "properties" : {
                key : item._GetSchema() for key, item in self.items()
            }
        }

import copy
from typing import Any

class NamedList(dict, _copyCallable):
    """Represents a Dictionary with an arbitrary number 
    of keys where the values need to satisfy the default_member."""
    def __init__(self, items:dict = None, default_member = None, comment = ""):
        self.comment = comment
        self.default_member = default_member or ConfigValue()
        if items: self.Set( items )

    def Set(self, data:dict):
        self.clear()
        for key, item in data.items():
            self[key] = copy.deepcopy( self.default_member )
            self[key].Set( item )
    
    def _GetSchema(self):
        return {
            "description" : self.comment,
            "type" : "object",
            "additionalProperties": self.default_member._GetSchema()
        }


class CollectionList(list, _copyCallable):
    """Represents a list or array of values which need to fullfill the default_member."""
    def __init__(self,items:list = None, default_member = None, comment = ""):
        self.comment = comment
        self.default_member = default_member or ConfigValue()
        if items: self.Set( items )

    def Set(self, data:list):
        self.clear()
        for index, item in enumerate( data ):
            value = None
            if isinstance( item, dict): value = CollectionDict( item )
            if isinstance( item, list): value = CollectionList( item )
            else: 
                value = copy.deepcopy( self.default_member )
                value.Set( item )
            self.append( value )
    
    def _GetSchema(self):
        return {
            "description" : self.comment,
            "type" : "array",
            "items": self.default_member._GetSchema()
        }

import json

class Collection(CollectionDict, _copyCallable):
    def __init__(self, items: dict = None):
        super().__init__(items)
    
    def To_Json(self, indent = 4):
        def default( data ):
            if hasattr( data, "_to_json"): return data._to_json()
            return json.JSONEncoder.default(self, data)
        return json.dumps( self, default=default, indent = indent)
    
    def From_Json(self, jsonstring:str):
        data = json.loads( jsonstring )
        self.Set( data )
    

    def _GetSchema(self):
        propertiesDict = {}
        for key, item in self.items():
            try:
                propertiesDict[key] = item._GetSchema()
            except AttributeError:
                pass
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://example.com/product.schema.json",
            "title": "TouchdesignerConfig",
            "description": "A dynamic and schemabased jsonConfig for Touchdesigner",
            "type": "object",
            "properties" : propertiesDict
        }
    

from typing import Type
class SchemaObjects :
    ConfigValue = Type[ConfigValue]
    EnumValue = Type[EnumValue]
    NamedList = Type[NamedList]
    CollectionDict = Type[CollectionDict]
    CollectionList = Type[CollectionList]