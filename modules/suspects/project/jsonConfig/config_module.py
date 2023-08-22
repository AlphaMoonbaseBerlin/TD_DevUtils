


'''Info Header Start
Name : config_module
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

class ConfigValue:
    def _to_json(self):
        return self.Value

    def __repr__(self) -> str:
        return str( self.value.val )
    
    def __init__(self, 
                default = "", 
                validator = lambda value: True, 
                comment = "", 
                parser = None,
                typecheck = object):
        self.comment = comment
        self.validator = validator
        self.value = tdu.Dependency(None)
        self.parser = parser or type(default)
        self.typecheck = typecheck
        self.Set( default )

    def validate(self, value):
        if not isinstance(value, self.typecheck):
            return False, f"Invalid type. Expected {self.typecheck} got {type(value)}"
        if not self.validator( value ):
            return False, f"Validation requirement not satisfied"
        return True, "Pass"
        
    def Set(self, value):
        valid, errorstring = self.validate( value )
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


class CollectionDict(dict):
    def __init__(self, items:dict = None, comment = ""):
        self.comment = comment
        if items: self.update( items )
        
    def __getattr__(self, key):
        return self.get( key )
    
    def Set(self, data):
        for key, item in data.items():
            if key in self: self[key].Set( item )

import copy

class CollectionList(list):
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
    

import json

class Collection(CollectionDict):
    def __init__(self, items: dict = None):
        super().__init__(items)
    
    def To_Json(self, indent = 4):
        def default( data ):
            if hasattr( data, "_to_json"): return data._to_json()
            return json.JSONEncoder.default(self, o)
        return json.dumps( self, default=default, indent = indent)
    
    def From_Json(self, jsonstring:str):
        data = json.loads( jsonstring )
        self.Set( data )
    
